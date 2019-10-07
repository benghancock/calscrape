"""
A Python module for scraping and parsing federal judicial calendars
"""

import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class CalendarParser():
    """A court calendar parser object"""

    def __init__(self, base_url, calendar_index):
        """Initialize parsed calendar's objects"""

        # Attributes needed for scraping
        self.base_url = base_url
        self.calendar_index = calendar_index

        # Formats to output dates
        self.time_format = '%I:%M%p'
        self.date_format = '%A, %b %d %Y'

        # Regex patterns to detect times and dates on calendars
        self.cal_datepat = r'\b\w.+\d+.201\d\b'
        self.cal_timepat = r'\d+:\d+\w+(AM|PM)'
        self.cal_hearingpat = r'^(\d:\d\d-[a-zA-Z]+-\d+-[a-zA-Z]+)\s-\s(.*)$'


class CANDParser(CalendarParser):
    """A parser for the California Northern District court"""

    def __init__(self, base_url, calendar_index):
        """
        Initialize attributes of the parent class;
        then initialize attributes needed for child class
        """
        super().__init__(base_url, calendar_index)

    def grab_court_index(self):
        """Return the scraped court calendar index page"""
        index_page = requests.get(self.calendar_index)

        return index_page.text

    def scrape_index(self, index_page):
        """Return a dict of calendar URLs from the index page HTML"""
        parsed_index = {}

        # Index page is organized as a table, get table rows ('tr')
        soup = BeautifulSoup(index_page, 'lxml')
        rows = soup.find_all('tr')

        for row in rows:
            judge_name = row.th.a.text.strip()
            url_ending = row.th.a['href'].strip()
            calendar_url = self.base_url + url_ending

            parsed_index[judge_name] = calendar_url

        return parsed_index

    def scrape_calendars(self, testing=False):
        """
        Takes a dict of judge names and URLs
        returns a dict of requests 'Response' objects
        """
        calendars = {}

        for judge, url in self.calendar_urls.items():
            r = requests.get(url)
            calendars[judge] = r

            if testing:          # Break after one scrape
                break

            else:
                time.sleep(.5)   # Slow down the scrape
                continue

        self.calendars = calendars

    def parse_calendar(self, calendar):
        """Parse all hearing information on a given CAND judge's calendar"""

        hearing_data = []

        calendar_soup = BeautifulSoup(calendar, 'lxml')

        # Get the judge's name from string
        page_top = str(calendar_soup.find('a', attrs={'name': '#top'}))
        judge_name = re.search(r'Calendar for: (\w.*?)<br/>', page_top).group(1)

        # Calendar is organized as a table, get table rows ('tr')
        table = calendar_soup.find('table', attrs={'class': 'Calendar'})

        # Handle the possibility of an empty calendar
        try:
            # Only get nonempty cells in the table
            table_data = table.find_all(text=True)

            for cell in table_data:
                court_date = re.search(self.cal_datepat, cell)
                court_time = re.search(self.cal_timepat, cell)
                hearing = re.search(self.cal_hearingpat, cell)
                # TODO Parse and grab under seal case captions

                if court_date:
                    try:
                        hearing_date = datetime.strptime(
                                court_date.group(), self.date_format
                                ).date()

                    except ValueError:
                        pass

                if court_time:
                    try:
                        hearing_time = datetime.strptime(
                                court_time.group(), self.time_format).time()
                    except ValueError:
                        pass

                if hearing:
                    date_stamp = datetime.combine(hearing_date,
                                                  hearing_time)

                    # Details of hearing are at next index location in list
                    hearing_detail = table_data[table_data.index(cell) + 1]

                    data = {'judge': judge_name,
                            'date': date_stamp,
                            'case_no': hearing.group(1),
                            'case_cap': hearing.group(2),
                            'detail': hearing_detail}

                    hearing_data.append(data)

                else:
                    continue

        except AttributeError:
            pass

        return hearing_data
