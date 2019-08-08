#!/usr/bin/env python3

"""
Tests for the calendar_parser module
"""

import configparser
import unittest
import calendar_parser as calparse

CONFIG_FILE = '../calendars_conf.ini'
TEST_CAND_INDEX = "test_data/test_cand_index.html"


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


if __name__ == '__main__':
    unittest.main()
