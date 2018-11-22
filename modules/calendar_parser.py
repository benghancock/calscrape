"""Python module for scraping and parsing federal judicial calendars"""

import requests
from bs4 import BeautifulSoup

class CalendarParser():
    """A court calendar parser object"""

    def __init__(self, base_url, calendar_index):
        """Initialize parsed calendar's objects"""

        # Attributes needed for scraping
        self.base_url = base_url
        self.calendar_index = calendar_index

        # Attributes of court calendar items
        self.courtdates = []
        self.time_format = '%I:%M%p'
        self.date_format = '%A, %b %d %Y'
        self.cal_dateformat = r'\b\w.+\d+.201\d\b'
        self.cal_timepattern = r'\d+:\d+\w+(AM|PM)'

    def cook_lxml(self, url):
        """Return a BeautifulSoup object for a given calendar URL using LXML"""
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')

        return soup

class CANDParser(CalendarParser):
    """A parser for the California Northern District court"""

    def __init__(self, base_url, calendar_index):
        """
        Initialize attributes of the parent class;
        then initialize attributes needed for child class
        """
        super().__init__(base_url, calendar_index)

    def scrape_calendars(self):
        """Dynamically scrape the calendars listed at the base URL"""
        soup = self.cook_lxml(self.calendar_index)

        # Court calendars are organized as a table
        rows = soup.find_all('tr')

        for row in rows:
            judge_name = row.th.a.text.strip()
            url_ending = row.th.a['href'].strip()

            sub_url = self.base_url + url_ending
            judge_calendar = self.cook_lxml(sub_url)

            print(judge_name)
            print(judge_calendar.a.strong)
