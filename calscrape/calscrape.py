#!/usr/bin/env python3

"""
CalScrape: rapidly scrape and search judicial calendars
"""

import argparse
import configparser
from datetime import datetime
from dateutil import tz
import logging
import os
import pkg_resources
from pathlib import Path

from .version import __version__
from .calendar_parser import CANDParser
from .hearings import load_hearings, Hearings
from .scrape_outputter import output_csv


SUPPORTED_COURTS = ['CAND']
COURTS_CONFIG_FILE = "courts_config.ini"
LOCAL_SCRAPE_DATA = "calscrape_latest_scrape.json"
OUTPUT_OPTIONS = ["csv", "ical", "json", "plain"]

# Store latest scrape data
latest_scrape_path = os.path.join(
    Path.home(), LOCAL_SCRAPE_DATA
)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        prog='calscrape',
        description='scrape and search court hearing calendars'
    )

    parser.add_argument(
        '--court',
        required=True,
        choices=SUPPORTED_COURTS,
        help='short code for the desired court'
    )

    parser.add_argument(
        '--test',
        required=False,
        action='store_true',
        default=False,
        help='test mode'
    )

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        default=False,
        help="verbose logging to the console"
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--new",
        action="store_true",
        default=False,
        help="print hearings new since last scrape"
    )

    mode.add_argument(
        "--cancelled",
        action="store_true",
        default=False,
        help="print hearings cancelled since last scrape"
    )

    mode.add_argument(
        "--showall",
        action="store_true",
        default=False,
        help="print all scraped hearings to stdout"
    )

    mode.add_argument(
        "--find",
        type=str,
        help="find hearings with a search term in the case caption"
    )

    parser.add_argument(
        "--output",
        choices=OUTPUT_OPTIONS,
        required=False,
        default="json"
    )

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
        parser = CANDParser(config['CAND']['CAND_BASEURL'],
                            config['CAND']['CAND_INDEX'])
        return parser

    else:
        return None


def hearings_readable(hearing_data):
    """Print hearings to the console in a human-readable way"""
    print("--- BEGIN HEARINGS ---")
    for hearing in hearing_data:
        for key, value in hearing.items():
            print(f"{key}: {value}")

        print("---------------")

    print("NO MORE HEARINGS")

    return None


def find_by_caption(hearing_data, search_string):
    """Find hearings by string in the case caption"""
    matches = []

    for hearing in hearing_data:
        case_cap = hearing.get('case_cap')

        if search_string.lower() in case_cap.lower():
            matches.append(hearing)

        else:
            continue

    return matches


def main():
    # Resolve the path the .ini file
    courts_config_path = pkg_resources.resource_filename(
        __name__, COURTS_CONFIG_FILE
    )

    args = parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    else:
        logging.basicConfig(level=logging.ERROR)

    # TODO Handle FileNotFoundError for config file
    config = load_courts_config(courts_config_path)
    court = args.court.lower()
    testing = args.test
    output_format = args.output

    # Initialize the scraper
    scraper = select_court(court, config)

    # Grab all the calendar URLs to scrape
    index = scraper.grab_court_index()
    calendar_urls = scraper.scrape_index(index)

    # Conduct the scrape; TS is local time for the court
    court_config_code = court.upper()
    court_tz = tz.gettz(config[court_config_code]['TIMEZONE'])
    scrape_ts = datetime.now(court_tz)
    calendars = scraper.scrape_calendars(calendar_urls, testing)

    # Parse the raw calendar HTML
    parsed_calendars = []

    for judge, calendar in calendars.items():
        parsed_calendar = scraper.parse_calendar(calendar.text)
        parsed_calendars.extend(parsed_calendar)

    scrape = Hearings(
        hearing_data=parsed_calendars,
        scrape_ts=scrape_ts
    )

    # NEW HEARINGS OPTION: Print out only the new hearings
    if args.new:
        try:
            prior_scrape = load_hearings(latest_scrape_path)
            new = scrape.detect_new(prior_scrape)
            new_count = str(len(new))

            print(f"found {new_count} new hearings")
            print(new)

        except FileNotFoundError:
            print("cannot id new hearings ... file for prior scrape not found")

    # CANCELLED HEARINGS OPTION: Print out only the cancelled hearings
    elif args.cancelled:
        try:
            prior_scrape = load_hearings(latest_scrape_path)
            cancelled = scrape.detect_cancelled(prior_scrape)
            cancelled_count = str(len(cancelled))

            print(f"found {cancelled_count} cancelled hearings")
            print(cancelled)

        except FileNotFoundError:
            print("cannot id cancelled hearings ... "
                  "file for prior scrape not found")

    elif args.find:
        matches = find_by_caption(scrape.hearing_data, args.find)
        hearings_readable(matches)

    elif args.showall:
        hearings_readable(scrape.hearing_data)

    elif output_format == "csv":
        output_csv(scrape.hearing_data)

    # DEFAULT BEHAVIOR: Overwrite the prior scrape data
    logging.info("storing latest scrape data and exiting ...")
    scrape.store_scrape(latest_scrape_path)


if __name__ == '__main__':
    main()
