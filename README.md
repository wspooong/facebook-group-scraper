# Facebook Group Scraper

A Facebook group scraper, highly inspired by [kevinzg/facebook-scraper](https://github.com/kevinzg/facebook-scraper).

Written in Python 3.7. Not tested on other versions.

## Install

Install this package by git clone.

```bash
git clone https://github.com/wspooong/facebook-group-scraper.git
pip install -r requirements.txt
```

## Running the tests

```bash
pip install pytest== 7.2.2
pytest
```

## Usage

Here is an example of how to use this package:

```python
from facebook_group_scraper import GroupScraper

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

```

In the above code, `group_url` is the ID of the Facebook group you want to scrape. You can find this ID in the URL of the group's Facebook page.

`page_cursor` is used to paginate through the posts in the group. If `page_cursor` is `None`, the scraper will start from the most recent post and work its way backwards.

`fetch_comment` and `fetch_reply` are boolean values that determine whether or not to fetch comments and replies for each post. If set to `True`, the scraper will fetch all comments and replies for each post.

`page_sleep_secs`, `comment_sleep_secs`, and `reply_sleep_secs` are the number of seconds to sleep between each request. These values are useful for rate limiting your requests to Facebook's servers.

## Testing

This package comes with tests to ensure that it is working properly. To run the tests, first install the necessary dependencies:

```
pip install pytest responses
```

Then, run the tests:

```
pytest
```

## Contributing

If you find any bugs or have any suggestions for this package, feel free to open an issue or a pull request on the [GitHub repository](https://github.com/wspooong/facebook-group-scraper).

## Authors

- **Shih-Peng Wen** - _Initial work_ - [website](https://wspooong.com)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
