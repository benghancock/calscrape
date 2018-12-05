"""Python module for scraping and parsing federal judicial calendars"""

import re
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
        self.cal_hearingpat =  r'^(\d:\d\d-[a-zA-Z]+-\d+-[a-zA-Z]+)\s-\s(.*)$'

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
        """Dynamically scrape the calendars listed at the index URL"""
        soup = self.cook_lxml(self.calendar_index)

        # Index page is organized as a table, get table rows ('tr')
        rows = soup.find_all('tr')

        for row in rows:
            judge_name = row.th.a.text.strip()
            url_ending = row.th.a['href'].strip()

            sub_url = self.base_url + url_ending
            judge_calendar = self.cook_lxml(sub_url)

            if judge_calendar:
                hearings_data = self.parse_hearings(judge_name, judge_calendar)
                print(hearings_data)

            else:
                continue

    def parse_hearings(self, judge_name, calendar_soup):
        """Parse all hearing information on a given CAND judge's calendar"""
        # Start by just testing hearing times
        hearing_data = []

        # Calendar is organized as a table, get table rows ('tr')
        table = calendar_soup.find('table', attrs={'class':'Calendar'})

        try:
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    court_date = re.search(self.cal_datepat, cell.text)
                    court_time= re.search(self.cal_timepat, cell.text)

                    if court_time:
                        try:
                            hearing_time = datetime.strptime(court_time.group(),
                                                                  self.time_format).time()
                            data = {'judge': judge_name,
                                    'hearing_time': hearing_time}
                            hearing_data.append(data)
                            continue

                        except ValueError:
                            pass

                    else:
                        continue

        except AttributeError:
            pass

        return hearing_data
