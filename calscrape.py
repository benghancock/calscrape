#!/usr/bin/env python3

"""CalScrape - A tool for rapidly searching judicial calendars

This is the main script for scraping and returning calendar data.
"""

import json

from modules.spatula import Spatula
from modules.calparse import ParsedCal

VERSION = "1.0"
SUPPORTED_CALENDARS = ['cand']


def greet_user(version, supported):
    """Greet the user and provide basic info about the program"""
    greeting = "\nCalScrape: Rapidly search judicial calendars"
    version_line = f"version {version}"

    print(greeting)
    print(version_line)

    print("\nThe following courts are currently supported:")

    for court in supported:
        print("- " + court.upper())


def prompt_user():
    """Prompt the user and check for supported calendars

    Expects list as arg
    """
    print("\nEnter the code of the court to be searched:")

    while True:

        selection = input("\nSelection >> ").lower()

        if selection == "q":
            return None

        elif selection in SUPPORTED_CALENDARS:
            return selection

        else:
            print("Not a valid selection.")


def pick_mode():
    """Prompts for list-based or single keyword search mode"""
    prompt = "\nPlease pick a search mode."
    prompt += "\nEnter \"keyword\" for a single keyword search,"
    prompt += "\nor enter \"list\" for a list-based search."
    print(prompt)

    prompting = True
    mode = None

    while prompting:

        mode = input("\nMode >> ")

        if mode == "keyword":
            prompting = False

        elif mode == "list":
            prompting = False

        else:
            print("Not a valid mode selection.")

    return mode


def load_calfile():
    """Load the calendars JSON file

    Expects arg `selection` as string
    """
    selection = prompt_user()

    try:
        with open(f"data/{selection}-urls.json") as f:
            calendars = json.load(f)

        return calendars

    except FileNotFoundError as e:
        print("No calendar file found for that court")
        print(f"Error: {e}")


def load_searchfile():
    """Load the search keys file in list mode"""
    searchterms = None

    try:
        with open("user/searchterms.json") as f:
            searchterms = json.load(f)

        return searchterms

    except FileNotFoundError as e:
        print("Could not find search term list file.")
        print(f"Error: {e}")

        return searchterms


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
    """Print neatly formatted results of calendar search"""

    greet_user(version=VERSION, supported=SUPPORTED_CALENDARS)

    while True:

        calfile = load_calfile()

        if calfile is None:
            return

        mode = pick_mode()
        results = []

        if mode == "keyword":
            searchterm = input("\nKeyword: ")

            print("Searching ...")

            for judge, url in calfile.items():
                page = Spatula(url)
                page.scrape()
                raw = page.serve_cand()

                cal = ParsedCal(raw)
                matches = cal.cand_search(searchterm, judge)

                # cand_search returns an empty list if there are no matches
                results.extend(matches)

        elif mode == "list":
            searchterms = load_searchfile()

            if searchterms is None:
                return

            else:

                print("Searching for the following terms...")
                for searchterm in searchterms:
                    print(searchterm, end=" ")

                print("\n")

                for judge, url in calfile.items():
                    page = Spatula(url)
                    page.scrape()
                    raw = page.serve_cand()

                    cal = ParsedCal(raw)

                    for searchterm in searchterms:
                        matches = cal.cand_search(searchterm,
                                                  judge)

                        results.extend(matches)

        if not results:
            print("No matches")

        else:
            results_ordered = sorted(results,
                                     key=lambda k: k['date'])
            read_results(results_ordered)

        return


if __name__ == "__main__":
    main()
