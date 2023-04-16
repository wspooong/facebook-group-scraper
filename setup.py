"""Setup script for facebook-group-scraper."""
from setuptools import setup

setup(
    name="facebook-group-scraper",
    version="0.1",
    python_requires="==3.7.*",
    description="Scrape Facebook group posts",
    url="https://github.com/wspooong",
    author="wspooong",
    author_email="wspooong@gmail.com",
    packages=["facebook-group-scraper"],
    install_requires=[
        "requests",
        "lxml",
    ],
)
