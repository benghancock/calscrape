"""A module to deliver raw scraped court calendars."""

from lxml import html
import requests


class Spatula():
    """Scraped web content object for parsing"""

    def __init__(self, url):
        """Initialize attributes for scraper"""
        self.url = url
        self.tree = ''
        self.raw = ''

    def scrape(self):
        """Download the content and load the contents"""
        try:
            page = requests.get(self.url)

            # Use `content` because `fromstring` expects bytes as input
            self.tree = html.fromstring(page.content)
            return self.tree

        except requests.exceptions.RequestException as e:
            print("Connection error. Check internet connection")
            print("Received this error:")
            print(e)

    def serve_cand(self):
        """Serve up raw calendar data from the CAND court"""
        self.raw = self.tree.xpath('//td/text()')
        return self.raw
