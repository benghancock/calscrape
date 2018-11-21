"""Python module for scraping and parsing federal judicial calendars"""

import requests
from bs4 import BeautifulSoup

class CalendarParser():
    """A court calendar parser object"""

    def __init__(self, base_url):
        """Initialize parsed calendar's objects"""
        self.base_url = base_url
        self.courtdates = []
        self.time_format = '%I:%M%p'
        self.date_format = '%A, %b %d %Y'
        self.cal_dateformat = r'\b\w.+\d+.201\d\b'
        self.cal_timepattern = r'\d+:\d+\w+(AM|PM)'


class CANDParser(CalendarParser):
    """A parser for the California Northern District court"""

    def __init__(self, base_url):
        """
        Initialize attributes of the parent class
        Then initilize attributes needed for child class
        """
        super().__init__(base_url)

    def scrape_calendars(self):
       """Dynamically scrape the calendars listed at the base URL"""
       court_page = requests.get(self.base_url)
       court_soup = BeautifulSoup(court_page.text, 'lxml')

       # Court calendars are organized as a table
       rows = court_soup.find_all('tr')
       for row in rows:
           print(row.th.a.text.strip())
