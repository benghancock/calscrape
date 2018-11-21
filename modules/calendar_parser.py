"""Python module for scraping and parsing federal judicial calendars"""

import requests
from bs4 import BeautifulSoup

class CalendarParser():
    """A court calendar parser object"""

    def __init__(self, base_url):
        """Initialize parsed calendar's objects"""
        self.base_url = base_url
        self.soup = ''
        self.courtdates = []
        self.time_format = '%I:%M%p'
        self.date_format = '%A, %b %d %Y'
        self.cal_dateformat = r'\b\w.+\d+.201\d\b'
        self.cal_timepattern = r'\d+:\d+\w+(AM|PM)'

    def cook_soup(self):
        """Return a BeautifulSoup object for the base calendar URL"""
        court_page = requests.get(self.base_url)
        self.soup = BeautifulSoup(court_page.text, 'lxml')

        return self.soup

    def more_soup(self, sub_url):
        """Return a BeautifulSoup object for individual calendars"""
        calendar_page = requests.get(sub_url)
        calendar_soup = BeautifulSoup(calendar_page.text, 'lxml')

        return calendar_soup

class CANDParser(CalendarParser):
    """A parser for the California Northern District court"""

    def __init__(self, base_url):
        """
        Initialize attributes of the parent class;
        then initialize attributes needed for child class
        """
        super().__init__(base_url)

    def scrape_calendars(self):
        """Dynamically scrape the calendars listed at the base URL"""
        self.cook_soup()

        # Court calendars are organized as a table
        rows = self.soup.find_all('tr')

        for row in rows:
            judge_name = row.th.a.text.strip()
            url_ending = row.th.a['href'].strip()
            sub_url = "%s%s" % (self.base_url, url_ending)
            judge_calendar = self.more_soup(sub_url)

            print(judge_name)
            #TODO! Test grabbing correct calendar
