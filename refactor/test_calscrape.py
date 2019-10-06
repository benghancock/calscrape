#!/usr/bin/env python 3

"""
Tests for calscrape.py and modules
"""


import unittest

import calscrape
import calendar_parser

TEST_CAND_INDEX = 'test_data/test_cand_index.html'
TEST_JUDGE_PAGE = 'test_data/test_judge_page.html'


class TestCalscrape(unittest.TestCase):

    def test_select_court(self):
        config = calscrape.load_courts_config()
        test_court = "CAND"
        court = calscrape.select_court(test_court, config)
        self.assertIsInstance(court, calendar_parser.CANDParser)


class TestCalendarparser(unittest.TestCase):

    def setUp(self):
        """Set up necessary elements for testing"""
        config = calscrape.load_courts_config()
        test_court = "CAND"
        self.court = calscrape.select_court(test_court, config)

        self.test_judge_name = "Alsup, William H. [WHA]"
        self.test_judge_url = "https://www.cand.uscourts.gov/CEO/cfd.aspx?7137"

        self.test_court_index = open(TEST_CAND_INDEX)
        self.test_judge_page = open(TEST_JUDGE_PAGE)

    def tearDown(self):
        """Close test data files"""
        self.test_court_index.close()
        self.test_judge_page.close()

    def test_scrape_index(self):
        """
        Test method for retrieving court index
        Should return dictionary with judge's name and correct URL
        """
        court_index = self.court.scrape_index(self.test_court_index)
        self.assertEqual(court_index.get(self.test_judge_name),
                         self.test_judge_url)
        


if __name__ == '__main__':
    unittest.main()
