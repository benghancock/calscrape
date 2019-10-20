#!/usr/bin/env python3

"""
Tests for calscrape.py and modules
"""

from datetime import datetime, timezone, timedelta
import unittest

import calscrape
import calendar_parser
from dateutil import tz
import hearings

TEST_CAND_INDEX = 'test_data/test_cand_index.html'
TEST_JUDGE_PAGE = 'test_data/test_judge_page.html'
COURTS_CONFIG = "courts_config.ini"


class TestCalscrape(unittest.TestCase):

    def test_select_court(self):
        config = calscrape.load_courts_config(COURTS_CONFIG)
        test_court = "CAND"
        parser = calscrape.select_court(test_court, config)
        self.assertIsInstance(parser, calendar_parser.CANDParser)


class TestCalendarparser(unittest.TestCase):

    def setUp(self):
        """Set up necessary elements for testing"""
        config = calscrape.load_courts_config(COURTS_CONFIG)
        test_court = "CAND"
        self.parser = calscrape.select_court(test_court, config)

        self.test_court_index = open(TEST_CAND_INDEX)
        self.test_judge_page = open(TEST_JUDGE_PAGE)
        self.test_judge_name = "Alsup, William H. [WHA]"
        self.test_judge_url = "https://www.cand.uscourts.gov/CEO/cfd.aspx?7137"

        self.test_tz = timezone(timedelta(hours=-7))

    def tearDown(self):
        """Close test data files"""
        self.test_court_index.close()
        self.test_judge_page.close()

    def test_scrape_index(self):
        """
        Test method for retrieving court index
        Should return dictionary with judge's name and correct URL
        """
        court_index = self.parser.scrape_index(self.test_court_index)
        self.assertEqual(court_index.get(self.test_judge_name),
                         self.test_judge_url)

    def test_parse_calendar(self):
        calendar = self.parser.parse_calendar(self.test_judge_page)
        test_hearing = calendar[0]
        self.assertEqual(test_hearing.get("judge"), "Judge William Alsup")
        self.assertEqual(test_hearing.get("date"),
                         datetime(2019, 9, 18, 10, tzinfo=self.test_tz))
        self.assertEqual(test_hearing.get("case_no"), "3:19-cv-01454-WHA")
        self.assertEqual(test_hearing.get("case_cap"),
                         "Drevaleva v. United States of America et al")
        self.assertEqual(test_hearing.get("detail"), "Motion to Dismiss")


class TestHearings(unittest.TestCase):

    def setUp(self):
        config = calscrape.load_courts_config(COURTS_CONFIG)
        test_court = "CAND"
        self.parser = calscrape.select_court(test_court, config)
        with open(TEST_JUDGE_PAGE) as p:
            self.test_data = self.parser.parse_calendar(p)

        self.test_latest = self.test_data[:3]
        self.test_prior = self.test_data[:2]
        self.test_tz = tz.gettz('America/Los_Angeles')
        self.test_scrape_time = datetime(2019, 10, 1, tzinfo=self.test_tz)

    def test_detect_new(self):
        """A method for detecting new hearings"""
        latest_scrape = hearings.Hearings(self.test_latest)
        self.assertTrue(latest_scrape.hearing_data == self.test_latest)
        self.assertTrue(len(latest_scrape.hearing_data) == 3)

        new = latest_scrape.detect_new(self.test_prior)
        self.assertTrue(len(new) == 1)
        self.assertTrue(new[0] == self.test_data[2])

    def test_detect_cancelled(self):
        """A method for detecting cancelled hearings"""
        mock_prior = hearings.Hearings(self.test_data[:3])
        mock_latest = hearings.Hearings(self.test_data[:2])

        cancelled = mock_latest.detect_cancelled(mock_prior)
        self.assertTrue(cancelled[0] == self.test_data[2])

    def test_make_set(self):
        """Turn a list of dictionaries into a set for comparison"""
        data = [{'a': 'b', 'c': 'd'}, {'e': 'f', 'g': 'h'}]
        test_hearings = hearings.Hearings(data)
        set_data = test_hearings.make_set(test_hearings.hearing_data)
        self.assertTrue(
            set_data == {(('e', 'f'), ('g', 'h')), (('a', 'b'), ('c', 'd'))}
            )

    def test_revert_list(self):
        """Revert a set of tuple elements back to a list of dictionaries"""
        data = [{'a': 'b', 'c': 'd'}, {'e': 'f', 'g': 'h'}]
        test_hearings = hearings.Hearings(data)

        set_data = {(('e', 'f'), ('g', 'h')), (('a', 'b'), ('c', 'd'))}
        reverted = test_hearings.revert_list(set_data)

        # sort the reverted list
        reverted = sorted(reverted, key=lambda x: list(x.keys()))
        self.assertTrue(data[1] == reverted[1])


if __name__ == '__main__':
    unittest.main()
