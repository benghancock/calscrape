#!/usr/bin/env python3
import argparse
from datetime import datetime
import logging
from pprint import pformat
import re

from bs4 import BeautifulSoup
import requests
import requests.exceptions

log = logging.getLogger(__name__)

BASE_URL = 'http://www.nysb.uscourts.gov'
CALENDAR_URL = BASE_URL + '/calendars-0'


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_const',
                        dest='verbosity', const=logging.DEBUG,
                        default=logging.INFO,
                        help='set log level to DEBUG')
    parser.add_argument('-t', '--test', action='store_true',
                        help='break before scraping all urls')
    parser.add_argument('--url', default=CALENDAR_URL)

    args = parser.parse_args()
    return args


def parse_judge(calendar):
    args = parse_args()

    hearings = []

    try:
        judge_name = calendar.find('div', attrs={'id': 'location'}).text.strip()
        log.info(judge_name)
    except AttributeError:
        return []

    dates = calendar.find_all('div',
                              attrs={'id': re.compile(r'^d\d{4}-\d{1,2}-\d{1,2}')})

    for judge_day in dates:
        date_str = judge_day.find('p').text.strip()
        # TODO Are days of the month zero-padded?
        hearing_date = datetime.strptime(date_str, '%A, %B %d, %Y').date()

        # TODO Parse date only once after ensuring there are no anomalies.
        if args.test:
            date_from_id = judge_day.get('id')
            date_from_id = datetime.strptime(date_from_id, 'd%Y-%m-%d').date()
            assert date_from_id == hearing_date

        try:
            rows = judge_day.find('table').find_all('tr')
        except AttributeError:
            continue

        for row in rows:
            # print(row.prettify())

            for cell in row.find_all('td'):
                # TODO Find a more elegant way to parse with BeautifulSoup.
                row_data = ' '.join(cell.text.split())
                hearing_details = cell.get_text('\n').strip()

                try:
                    hearing_time = datetime.strptime(row_data, '%I:%M %p').time()
                    timestamp = datetime.combine(hearing_date, hearing_time)
                    continue
                except ValueError:
                    pass

                # TODO Is this a standard ID format?
                if re.compile(r'^\d+-\d+-[a-z]+ ').match(row_data):
                    header = row_data
                elif row_data:
                    structured_data = {'judge name': judge_name,
                                       'timestamp': timestamp,
                                       'header': header,
                                       'case details': hearing_details}
                    log.debug(f'\n{pformat(structured_data)}\n')

                    hearings.append(structured_data)

                    if args.test:
                        break
        if args.test:
            break

    return hearings


def main():
    args = parse_args()

    log.setLevel(args.verbosity)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                  '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    district_hearings = []

    calendars = requests.get(CALENDAR_URL)
    soup = BeautifulSoup(calendars.text, 'lxml')
    urls = [a['href']
            for a
            in soup.find('div', attrs={'class': 'field--name-body'}).find_all('a')]

    for url in urls:
        log.debug(f'{BASE_URL + url}')
        try:
            calendar = BeautifulSoup(requests.get(BASE_URL + url).text, 'lxml')
        except requests.exceptions.ConnectionError:
            continue

        district_hearings.extend(parse_judge(calendar))

        if args.test:
            break

    log.info(f'District hearing count: {len(district_hearings)}')


if __name__ == '__main__':
    main()
