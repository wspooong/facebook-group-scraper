"""A Example for using the Facebook Group Scraper."""
from src.facebook_group_scraper import GroupScraper
import json
import logging

logging.basicConfig(level=logging.INFO)

scraper = GroupScraper(
    group_url="1260448967306807",
    page_cursor=None,
    fetch_comment=True,
    fetch_reply=True,
    page_sleep_secs=10,
    comment_sleep_secs=5,
    reply_sleep_secs=3,
)

for post in scraper.start():
    # Do something with the post
    print(post["post_id"])
    print(post["content"])
    print("=" * 20)
    with open("test.jsonl", "a+") as f:
        _ = f.write(json.dumps(post, ensure_ascii=False))
        _ = f.write("\n")
