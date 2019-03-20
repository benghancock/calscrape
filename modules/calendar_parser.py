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

    def get_lxml(self, url):
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
        """Dynamically scrape the calendars listed at the index URL"""
        calendars = []
        soup = self.get_lxml(self.calendar_index)

        # Index page is organized as a table, get table rows ('tr')
        rows = soup.find_all('tr')

        for row in rows:
            judge_name = row.th.a.text.strip()
            url_ending = row.th.a['href'].strip()

            sub_url = self.base_url + url_ending
            judge_calendar = self.get_lxml(sub_url)
            time.sleep(.5)  # Slow down the scrape

            if judge_calendar:
                calendar_data = self.parse_hearings(judge_name, judge_calendar)
                calendars.extend(calendar_data)

            else:
                continue

        return calendars

    def parse_hearings(self, judge_name, calendar_soup):
        """Parse all hearing information on a given CAND judge's calendar"""

        hearing_data = []

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
                # TODO Grab hearing details
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
