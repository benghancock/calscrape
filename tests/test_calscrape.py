#!/usr/bin/env python3

"""
Tests for calscrape.py and modules
"""

from datetime import datetime, timezone, timedelta
from dateutil import tz
import unittest

import calscrape
import calendar_parser
import hearings

TEST_CAND_INDEX = 'test_data/test_cand_index.html'
TEST_JUDGE_PAGE = 'test_data/test_judge_page.html'
TEST_LOCAL_SCRAPE_FILE = 'test_data/test.json'
COURTS_CONFIG = "courts_config.ini"

################################
# Sample data to use for testing
################################

test_timezone = tz.gettz('America/Los_Angeles')

# Create a mock object for a previous scrape
sample_data_a = [
    {
        "judge": "Judge Judy",
        "case_cap": "Very Angry v. Somewhat Bewildered",
        "detail": "Motion to Dismiss",
        "date": datetime(2019, 11, 1, 8, tzinfo=test_timezone)
    },
    {
        "judge": "Judge Judy",
        "case_cap": "Zerg v. Terran",
        "detail": "Motion for TRO",
        "date": datetime(2019, 11, 5, 10, tzinfo=test_timezone)
    },
    {
        "judge": "Judge Judy",
        "case_cap": "Alien v. Predator",
        "detail": "Motion for Facehugger Removal",
        "date": datetime(2020, 1, 1, 16, tzinfo=test_timezone)
    }
]

sample_a_timestamp = datetime(2019, 11, 1, 0, tzinfo=test_timezone)
sample_hearings_a = hearings.Hearings(
    hearing_data=sample_data_a,
    scrape_ts=sample_a_timestamp
)

# Create a mock object for the most recent scrape
sample_data_b = [
    {
        "judge": "Judge Judy",
        "case_cap": "Very Angry v. Somewhat Bewildered",
        "detail": "Motion to Dismiss",
        "date": datetime(2019, 11, 1, 8, tzinfo=test_timezone)
    },
    {
        "judge": "Judge Judy",
        "case_cap": "Zerg v. Terran",
        "detail": "Motion for TRO",
        "date": datetime(2019, 11, 5, 10, tzinfo=test_timezone)
    },
    {
        "judge": "Judge Judy",
        "case_cap": "Pig v. Bird",
        "detail": "Status Conference",
        "date": datetime(2021, 1, 9, 15, tzinfo=test_timezone)
    }
]

sample_b_timestamp = datetime(2019, 11, 7, 0, tzinfo=test_timezone)
sample_hearings_b = hearings.Hearings(
    hearing_data=sample_data_b,
    scrape_ts=sample_b_timestamp
)

# An example of a newly detected hearing
newly_detected = [
    {
        "judge": "Judge Judy",
        "case_cap": "Pig v. Bird",
        "detail": "Status Conference",
        "date": datetime(2021, 1, 9, 15, tzinfo=test_timezone)
    }
]

# An example of a cancelled hearing
cancelled_hearing = [
    {
        "judge": "Judge Judy",
        "case_cap": "Alien v. Predator",
        "detail": "Motion for Facehugger Removal",
        "date": datetime(2020, 1, 1, 16, tzinfo=test_timezone)
    }
]

# An example of a hearing found in a search
found_hearing = [
    {
        "judge": "Judge Judy",
        "case_cap": "Alien v. Predator",
        "detail": "Motion for Facehugger Removal",
        "date": datetime(2020, 1, 1, 16, tzinfo=test_timezone)
    }
]


################################
# Test Fixtures
################################


class TestCalscrape(unittest.TestCase):

    def test_select_court(self):
        config = calscrape.load_courts_config(COURTS_CONFIG)
        test_court = "CAND"
        parser = calscrape.select_court(test_court, config)
        self.assertIsInstance(parser, calendar_parser.CANDParser)

    def test_find_by_caption(self):
        search_string = "alien"
        matches = calscrape.find_by_caption(
            sample_hearings_a.hearing_data,
            search_string
        )

        self.assertTrue(matches[0] == found_hearing[0])


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
        # FIXME Update to reflect the new index structure
        # court_index = self.parser.scrape_index(self.test_court_index)
        # self.assertEqual(court_index.get(self.test_judge_name),
        #                  self.test_judge_url)

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

    def test_detect_new(self):
        """A method for detecting new hearings"""
        new = sample_hearings_b.detect_new(sample_hearings_a)
        self.assertTrue(new[0] == newly_detected[0])

    def test_detect_cancelled(self):
        """A method for detecting cancelled hearings"""
        cancelled = sample_hearings_b.detect_cancelled(sample_hearings_a)
        self.assertTrue(cancelled[0] == cancelled_hearing[0])

    def test_store_scrape(self):
        """Store the latest scrape locally as json"""
        sample_hearings_b.store_scrape(TEST_LOCAL_SCRAPE_FILE)

    def test_load_scrape(self):
        """Load up the local scrape file and make sure it's the same"""
        scrape = hearings.load_hearings(TEST_LOCAL_SCRAPE_FILE)
        self.assertTrue(scrape.hearing_data == sample_hearings_b.hearing_data)
        self.assertTrue(scrape.scrape_ts == sample_hearings_b.scrape_ts)


if __name__ == '__main__':
    unittest.main()
