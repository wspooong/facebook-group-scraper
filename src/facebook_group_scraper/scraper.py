"""This module contains the GroupScraper class."""
import json
import logging
import re
import urllib.parse
from time import sleep
from typing import Generator

import requests
from lxml import etree

from src.facebook_group_scraper.utils import extract_digits
from src.facebook_group_scraper.constants import MOBILE_BASIC_URL, headers


class GroupScraper:
    """
    This class is used to scrape a Facebook group.

    Args:
        group_url (str): The URL of the Facebook group to scrape.
        fetch_comment (bool, optional): Whether to fetch comments. Defaults to True.
        fetch_reply (bool, optional): Whether to fetch replies. Defaults to True.
        page_cursor (str, optional): The URL for the next page. Defaults to None.
        page_sleep_secs (int, optional): Number of seconds to wait before scraping the next page. Defaults to 10.
        comment_sleep_secs (int, optional): Number of seconds to wait before scraping the next comment. Defaults to 5.
        reply_sleep_secs (int, optional): Number of seconds to wait before scraping the next reply. Defaults to 3.

    Methods:
        __init__(): Initializes the GroupScraper class.
        __repr__(): Returns a string representation of the GroupScraper class.
        start(): Yields a parsed post.
        _iter_page(): Iterates over each page in the Facebook group.
        _post_parser(): Parses the data of each post.
        _generate_next_page_url(): Generates the next page URL aka page_cursor.

    """

    def __init__(
        self,
        group_url: str,
        fetch_comment: bool = True,
        fetch_reply: bool = True,
        page_cursor: str = None,
        page_sleep_secs: int = 10,
        comment_sleep_secs: int = 5,
        reply_sleep_secs: int = 3,
    ):
        """Initialize the GroupScraper class."""
        self.group_url = self._check_group_url(group_url)
        self.fetch_comment = fetch_comment
        self.fetch_reply = fetch_reply
        self.page_cursor = page_cursor
        self.page_sleep_secs = page_sleep_secs
        self.comment_sleep_secs = comment_sleep_secs
        self.reply_sleep_secs = reply_sleep_secs

    def __repr__(self):
        """Return a string representation of the GroupScraper class."""
        return f"Facebook Group Scraper: {self.group_url}"

    def start(self) -> dict:
        """Yield a parsed post."""
        logging.info(f"[SCRAPER: MAIN] Start scraping {self.group_url}.")
        post_generator = self._iter_page()
        for page in post_generator:
            post_list = page.xpath(
                '//div[@id="m_group_stories_container"]/section/article'
            )
            for item in post_list:
                post = self._post_parser(item)
                yield post

    def _check_group_url(self, group_url: str) -> str:
        """Check if the group URL is valid."""
        if group_url.startswith("https://www.facebook.com/groups/"):
            return group_url
        elif group_url.isnumeric():
            return f"https://www.facebook.com/groups/{group_url}"
        else:
            raise ValueError("Please provide a valid Facebook group URL or group ID.")

    def _iter_page(self) -> etree.Element:
        """Iterate over each page in the Facebook group."""
        if self.page_cursor:
            url = urllib.parse.urljoin(MOBILE_BASIC_URL, self.page_cursor)
        elif self.group_url.startswith("https://www.facebook.com/groups/"):
            url = self.group_url.replace("https://www", "https://m")

        while True:
            response = requests.get(
                url=url,
                headers=headers,
            )

            html = etree.HTML(response.content.decode())
            yield html

            next_cursor = self._generate_next_page_url(response.text)
            if next_cursor:
                logging.info(
                    f"[SCRAPER: MAIN] Next page detected. Sleep for {self.page_sleep_secs} secs..."
                )
                logging.debug(f"[SCRAPER: MAIN] PAGE_CURSOR: {next_cursor}")
                sleep(self.page_sleep_secs)
                url = next_cursor
            else:
                break

    def _post_parser(self, post: etree.Element) -> dict:
        """
        Parse the details of each post and returns a dictionary containing the details.

        Args:
            post (etree.Element): An HTML element containing the details of a post.

        Returns:
            dict: A dictionary containing the details of the post.
        """
        raw_json = post.xpath("./@data-ft")[0]
        data_ft = json.loads(raw_json)
        if data_ft.get("story_attachment_style"):
            post_type = data_ft["story_attachment_style"]
        else:
            post_type = "non-attached"

        post_data = {}

        if post_type == "album":
            post_data["photo_list"] = data_ft["photo_attachments_list"]
        elif post_type == "photo":
            post_data["post_list"] = [data_ft["photo_id"]]
        elif post_type == "non-attached":
            pass
        else:
            logging.critical(f"[SCRAPER: POST] A new post type '{post_type}' detect. ")
            logging.critical(
                "[SCRAPER: POST] raw_json will be stored in 'errors_new_type.jsonl'. "
            )
            with open("errors_new_type.jsonl", "a+") as f:
                f.write(json.dumps({"raw_json": raw_json}))
                f.write("\n")
            return

        post_data["page_id"] = data_ft["page_id"]
        if data_ft.get("mf_story_key"):
            post_data["post_id"] = data_ft["mf_story_key"]
        elif data_ft.get("top_level_post_id"):
            post_data["post_id"] = data_ft["top_level_post_id"]

        for key in data_ft["page_insights"].keys():
            post_data["publish_time"] = (
                data_ft["page_insights"]
                .get(key, {})
                .get("post_context", {})
                .get("publish_time", None)
            )
            if post_data["publish_time"]:
                break

        post_data["author_id"] = data_ft["content_owner_id_new"]
        post_data["author_name"] = post.xpath(
            """.//h3[contains(@data-gt, '{"tn":"C"}')]//a/text()"""
        )[0]
        post_data["content"] = post.xpath(
            """.//div[contains(@data-ft, '{"tn":"*s"}')]//text()"""
        )

        if post.xpath('.//span[@class="like_def _28wy"]/text()'):
            post_data["likes"] = extract_digits(
                post.xpath('.//span[@class="like_def _28wy"]/text()')[0]
            )
        else:
            post_data["likes"] = 0

        if post.xpath('.//span[@class="cmt_def _28wy"]/text()'):
            post_data["comments"] = extract_digits(
                post.xpath('.//span[@class="cmt_def _28wy"]/text()')[0]
            )
        else:
            post_data["comments"] = 0

        # Fetch comments.
        if self.fetch_comment == True and post_data["comments"] > 0:
            post_data["comments_full"] = []
            for comment in self._get_comments(post_id=post_data["post_id"]):
                post_data["comments_full"].append(comment)

        return {
            key: post_data.get(key, None)
            for key in [
                "page_id",
                "post_id",
                "publish_time",
                "author_id",
                "author_name",
                "post_list",
                "content",
                "likes",
                "comments",
                "comments_full",
            ]
        }

    def _generate_next_page_url(self, raw_html: str) -> str:
        """
        Generate the next page URL aka "page_cursor".

        Args:
            raw_html (str): The raw HTML content of the current page.

        Returns:
            str: The URL of the next page.
        """
        match = re.findall(r'href[=:]"(\/groups\/[^"]+bac=[^"]+)"', raw_html)
        if match:
            return urllib.parse.urljoin(MOBILE_BASIC_URL, match[0])
        else:
            return None

    def _get_comments(self, post_id: str = None, post_url: str = None) -> Generator:
        """
        Get comments for single POST. This will use a lot of requests to get comments.

        Args:
            post_id (str, optional): The ID of the post to fetch comments from.
                Defaults to None.
            post_url (str, optional): The URL of the post to fetch comments from.
                Defaults to None.

        Yields:
            dict: A dictionary representing a comment, including the comment author,
            ID, and content. If reply fetching is enabled, also includes replies to
            the comment.
        """
        if post_id and post_url:
            logging.critical(f"[SCRAPER: COMMENT] Please post_id or post_url only.")
            return

        if post_id:
            url = urllib.parse.urljoin(MOBILE_BASIC_URL, post_id)

        if post_url:
            url = post_url

        comments_count = 0

        while True:
            response = requests.get(url=url, headers=headers)
            html = etree.HTML(response.text)
            comments_list = html.xpath(
                '//div[contains(@id, "ufi")]//div[@data-sigil="comment"]'
            )
            for comment in comments_list:
                result = {
                    "author": comment.xpath('.//div[@class="_2b05"]/text()')[0],
                    "comment_id": comment.xpath(
                        './/div[@data-sigil="comment-body"]/@data-commentid'
                    )[0],
                    "content": comment.xpath(
                        './/div[@data-sigil="comment-body"]//text()'
                    ),
                }
                comments_count += 1
                yield result

                # Fetch replys
                more_reply = (
                    comment.xpath('.//div[@data-sigil="replies-see-more"]') != []
                )
                if self.fetch_reply and more_reply:
                    logging.debug("[SCRAPER: COMMENTS] Found replys.")
                    reply_generator = self._get_reply(
                        url=comment.xpath(
                            './/div[@data-sigil="replies-see-more"]/a/@href'
                        )[0],
                        comment_id=comment.xpath(
                            './/div[@data-sigil="comment-body"]/@data-commentid'
                        )[0],
                    )
                    for reply in reply_generator:
                        comments_count += 1
                        yield reply

            more_comments = "see_prev" in response.text
            if not more_comments:
                logging.info(
                    f"[SCRAPER: COMMENTS] End fetch comments. Total Comments: {comments_count}"
                )
                return result

            logging.info(
                f"[SCRAPER: COMMENTS] Fetch next page. Sleep {self.comment_sleep_secs} secs... Total Comments: {comments_count}"
            )
            sleep(self.comment_sleep_secs)
            url = urllib.parse.urljoin(
                MOBILE_BASIC_URL,
                html.xpath('//div[contains(@id, "see_prev")]/a/@href')[0],
            )

    def _get_reply(self, url, comment_id) -> Generator:
        """
        Get replys for COMMENT. This will use a lot of requests to get replys.

        Args:
            url (str): The URL of the comment's reply page.
            comment_id (str): The ID of the comment being replied to.

        Yields:
            dict: Each dictionary represents a single reply to the comment.
        """
        logging.debug("[SCRAPER: REPLYS] Start fetching replys.")
        reply_url = urllib.parse.urljoin(MOBILE_BASIC_URL, url)
        response = requests.get(reply_url, headers=headers)
        html = etree.HTML(response.text)
        reply_list = html.xpath('//div[@class="_55x2 _3u3w"]/div[@class="_2a_i"]')
        for reply in reply_list:
            result = {
                "author": reply.xpath('.//div[@class="_2b05"]/text()')[0],
                "comment_id": comment_id,
                "reply_id": reply.xpath(
                    './/div[@data-sigil="comment-body"]/@data-commentid'
                )[0],
                "content": reply.xpath('.//div[@data-sigil="comment-body"]//text()'),
            }
            yield result

        logging.debug(
            f"[SCRAPER: REPLYS] End fetching replys. Sleep {self.reply_sleep_secs} secs..."
        )
        sleep(self.reply_sleep_secs)
