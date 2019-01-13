#!/usr/bin/env python3

"""CalScrape - A tool for rapidly searching judicial calendars

This is the main module for scraping and returning calendar data.
"""

import argparse
import pprint
from modules.calendar_parser import *
from modules.calendarsconf import *

VERSION = "2.0-dev"
SUPPORTED_COURTS = ['cand']

courts_info = " ".join(SUPPORTED_COURTS)
version_info = f"version: {VERSION} | supported courts: {courts_info}"


def get_args():
    parser = argparse.ArgumentParser(
                description='Rapidly search judicial calendars')
    parser.add_argument('--version', action='version',
                        version=f'{version_info}')

    # Mode selection
    parser.add_argument('-c', '--court', required=True,
                        help='court to be scraped')

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-f', '--full', action='store_true',
                      help='print full scrape results to stdout')
    parser.add_argument('--silent', action='store_true',
                        help='run silently and save results to logfile')
    mode.add_argument('-k', '--keyword', 
                      help='print results matching keyword')
    parser.set_defaults(full=True)

    args = parser.parse_args()
    return args


def read_results(results):
    """Parse list of dicts to cleanly ouput results of search"""
    for result in results:
        judge = result.get('judge')
        date = result.get('date')
        formatted_date = date.strftime('%a %b %d %I:%M %p')
        case = result.get('case')
        details = result.get('details')

        print(f"Judge: {judge}")
        print(f"Date: {formatted_date}")
        print(f"Case: {case}")
        print(f"Hearing: {details}")
        print("\n")


def main():
    while True:
        args = get_args()

        court_select = args.court
        full_mode = args.full
        keyword_mode = args.keyword     # TODO implement keyword search
        silent_mode = args.silent       # TODO implement silent logging

        if court_select not in SUPPORTED_COURTS:
            print(f"{court_select} is not a supported court")
            break

        else:
            # TODO Find way to elegantly handle court selection
            # For now, just test this with the CANDParser()
            court = CANDParser(base_url=CAND_BASEURL,
                               calendar_index=CAND_INDEX)
            hearings = court.scrape_calendars()

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(hearings)

            break


if __name__ == "__main__":
    main()
