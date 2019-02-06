#!/usr/bin/env python3

"""CalScrape - A tool for rapidly searching judicial calendars

This is the main module for scraping and returning calendar data.
"""

import argparse
import json

from modules.court_select import select_court

VERSION = "2.0-dev"
SUPPORTED_COURTS = ['cand']

JSON_OUT = "hearings.json"

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
    mode.add_argument('--silent', action='store_true',
                      help='run silently and save results to logfile')
    mode.add_argument('-k', '--keyword',
                      help='print results matching keyword')

    # parser.set_defaults(full=True)

    args = parser.parse_args()
    return args


def print_hearings(hearing_data):
    """Parse list of dicts to cleanly output results of search"""

    ordered_data = sort_hearings_bydate(hearing_data)

    for hearing in ordered_data:
        judge = hearing.get('judge')
        date = hearing.get('date')
        formatted_date = date.strftime('%a %b %d %I:%M %p')
        case_no = hearing.get('case_no')
        case_cap = hearing.get('case_cap')

        print(f"Judge: {judge}")
        print(f"Date: {formatted_date}")
        print(f"Case Num: {case_no}")
        print(f"Hearing: {case_cap}")
        print("\n")


def reformat_date(hearing_entry):
    """Format a datetime object, return as string"""
    date = hearing_entry.get('date')
    formatted_date = date.strftime('%a %b %d %I:%M %p')
    hearing_entry['date'] = formatted_date


def save_hearings(f_name, hearing_data):
    """Save list of dicts as JSON file locally"""
    ordered_data = sort_hearings_bydate(hearing_data)

    for entry in ordered_data:
        reformat_date(entry)

    with open(f_name, 'w') as f_obj:
        json.dump(hearing_data, f_obj)


def sort_hearings_bydate(hearing_data):
    """Sort list of dicts by 'date' key"""
    ordered_data = sorted(hearing_data,
                          key=lambda k: k['date'])
    return ordered_data


def main():
    while True:
        args = get_args()
        court = args.court.lower()
        full_mode = args.full
        keyword_mode = args.keyword     # TODO implement keyword search
        silent_mode = args.silent       # TODO implement silent logging

        if court not in SUPPORTED_COURTS:
            print(f"{court} is not a supported court")
            break

        else:
            court_parser = select_court(court)

            print("scraping court website ... hang tight")
            hearing_data = court_parser.scrape_calendars()

            if full_mode:
                print_hearings(hearing_data)
                break

            elif silent_mode:
                # Raises Type Error; datetime objects not friendly with JSON
                save_hearings(JSON_OUT, hearing_data)
                print("done.")
                break

            elif keyword_mode:
                # TODO
                print("stuff")
                break

            else:
                print("Nothing to do.")
                break


if __name__ == "__main__":
    main()
