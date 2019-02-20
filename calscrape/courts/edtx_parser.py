#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
TODO
'''
from datetime import datetime, timedelta
import logging

from bs4 import BeautifulSoup
import requests


class EDTX():
    '''
    TODO
    '''
    def __init__(self, session=None):
        self.court_name = 'EDTX'
        self.logger = logging.getLogger(self.court_name)
        self.session = session or requests.Session()
        self.base_url = 'http://www.txed.uscourts.gov'
        self._calendar = []

    @property
    def calendar(self) -> list:
        '''
        TODO
        '''
        if not self._calendar:
            self.parse_court_calendar()
        return self._calendar

    def parse_court_calendar(self) -> None:
        '''
        TODO
        '''
        # Request court HTML.
        url_response = self.session.get(self.base_url + '/?q=hearing-schedules')
        html = url_response.content
        court_soup = BeautifulSoup(html, 'lxml')
        judges = court_soup.find_all('div', attrs={'class': 'views-row'})

        for judge in judges:
            judge_name = judge.find('div',
                                    attrs={'class':
                                           'views-field-title'}).text.strip()

            for date in judge.find_all('td', attrs={'class': 'rtecenter'}):
                date_url = date.find('a', href=True)['href']

                # Request judge calendar HTML.
                url_response = self.session.get(self.base_url + date_url)
                hearings = self.parse_date_calendar(url_response, judge_name)
                self._calendar.extend(hearings)

    @staticmethod
    def parse_date_calendar(url_response: requests.models.Response,
                            judge_name: str) -> list:
        '''
        TODO
        '''
        day_soup = BeautifulSoup(url_response.text, 'lxml')
        day_table = day_soup.find('table',
                                  attrs={'class':
                                         'casehtml_schedule_table'})
        rows = day_table.find_all('tr')

        parsed_hearings = []

        # The first row is a header.
        header = [cell.string.strip().lower()
                  for cell
                  in rows[0].find_all('td')]

        for row in rows[1:]:
            hearing = {'judge name': judge_name,
                       'url': url_response.url}

            # TODO Determine which is more readable
            # for index, cell in enumerate(row.find_all('td')):
            #     hearing.update({header[index]: cell.text.strip()})
            hearing.update(dict(zip(header, [cell.text.strip()
                                             for cell
                                             in row.find_all('td')])))

            hearing_date = datetime.strptime(hearing.pop('date'),
                                             '%m/%d/%Y').date()

            try:
                hearing_time = datetime.strptime(hearing.pop('time'),
                                                 '%I:%M').time()
                timestamp = datetime.combine(hearing_date,
                                             hearing_time)
                # Hearing times lack meridiem
                # TODO What is the earliest/latest hearing time?
                if timestamp.hour < 9:
                    timestamp += timedelta(hours=12)

                hearing['timestamp'] = timestamp

            # Some calendar rows have a date but no time.
            except ValueError:
                hearing['timestamp'] = hearing_date

            parsed_hearings.append(hearing)

        return parsed_hearings
