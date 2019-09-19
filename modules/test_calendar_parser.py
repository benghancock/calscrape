#!/usr/bin/env python3

"""
Tests for the calendar_parser module

Functions to test:
- DONE parse_calendars_listing
- DONE scrape_calendars
- TODO parse_hearings
"""

import configparser
from datetime import datetime
import unittest

from bs4 import BeautifulSoup
import requests

import calendar_parser as calparse


CONFIG_FILE = '../calendars_conf.ini'
TEST_CAND_INDEX = 'test_data/test_cand_index.html'
TEST_JUDGE_PAGE = 'test_data/test_judge_page.html'


class CANDParserTest(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.parser = calparse.CANDParser(config['CAND']['CAND_BASEURL'],
                                          config['CAND']['CAND_INDEX'])

    def test_parse_calendars_listing(self):
        judge_name = "Alsup, William H. [WHA]"
        judge_url = "https://www.cand.uscourts.gov/CEO/cfd.aspx?7137"

        with open(TEST_CAND_INDEX) as index_page:
            calendars_listing = self.parser.parse_calendars_listing(index_page)
            self.assertEqual(
                calendars_listing.get(judge_name), judge_url
            )

    def test_scrape_calendar(self):
        """Should return a list of requests 'Response' objects"""
        judge_name = "Alsup, William H. [WHA]"
        judge_url = "https://www.cand.uscourts.gov/CEO/cfd.aspx?7137"
        calendar_urls = {judge_name: judge_url}

        calendars = self.parser.scrape_calendars(calendar_urls)

        # This may break if the network is not active
        self.assertIs(type(
            calendars.get(judge_name)), requests.models.Response)

    def test_parse_hearings_case_no(self):
        """Return a list of dictionaries with parsed hearing data"""

        sample_hearings_case_no = []
        with open(TEST_JUDGE_PAGE) as f:
            soup = BeautifulSoup(f, 'lxml')

        judge_name = "Alsup, William H. [WHA]"

        parsed_calendar = self.parser.parse_hearings(judge_name, soup)

        for hearing in parsed_calendar:
            if hearing.get('case_no') == '3:19-cv-01454-WHA':
                sample_hearings_case_no.append(hearing)
                
            else:
                continue

        self.assertTrue(len(sample_hearings_case_no) == 1)

    def test_parse_heraings_date_time(self):
        """Return the correct number of hearings for a given date and time"""
        sample_hearings_date_time = []

        with open(TEST_JUDGE_PAGE) as f:
            soup = BeautifulSoup(f, 'lxml')

        judge_name = "Alsup, William H. [WHA]"
        parsed_calendar = self.parser.parse_hearings(judge_name, soup)

        for hearing in parsed_calendar:
            if hearing.get('date') == datetime(2019, 9, 26, 8, 00):
                sample_hearings_date_time.append(hearing)

            else:
                continue

        self.assertTrue(len(sample_hearings_date_time) == 7)


if __name__ == '__main__':
    unittest.main()
