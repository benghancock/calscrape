#!/usr/bin/env python3

"""
CalScrape: rapidly scrape and search judicial calendars
"""

import argparse
import configparser

import calendar_parser

COURTS_CONFIG = "courts_config.ini"


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='scrape and search court hearing calendars')

    parser.add_argument('--court', required=True,
                        help='short code for the desired court')

    parser.add_argument('--test', required=False, action='store_true',
                        default=False, help='test mode')

    args = parser.parse_args()
    return args


def load_courts_config(config_file):
    """Load hard-coded configurations"""
    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def select_court(court_string, config):
    """Return an instance of the correct court parser based on arg"""

    # California Northern District
    if court_string.lower() == 'cand':
        parser = calendar_parser.CANDParser(config['CAND']['CAND_BASEURL'],
                                            config['CAND']['CAND_INDEX'])
        return parser

    else:
        return None


def main():
    # TODO Handle FileNotFoundError for config file
    config = load_courts_config(COURTS_CONFIG)
    args = parse_args()
    court = args.court.lower()
    testing = args.test

    scraper = select_court(court, config)
    index = scraper.grab_court_index()
    calendar_urls = scraper.scrape_index(index)
    calendars = scraper.scrape_calendars(calendar_urls, testing)

    parsed_calendars = []

    for judge, calendar in calendars.items():
        parsed_calendar = scraper.parse_calendar(calendar)
        parsed_calendars.extend(parsed_calendar)

    print(parsed_calendars)


if __name__ == '__main__':
    main()
