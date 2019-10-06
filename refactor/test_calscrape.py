#!/usr/bin/env python 3

"""
Tests for calscrape.py and modules
"""


import unittest

import calscrape
import calendar_parser


class TestCalscrape(unittest.TestCase):

    def test_select_court(self):
        config = calscrape.load_courts_config()
        test_court = "CAND"
        court = calscrape.select_court(test_court, config)
        self.assertIsInstance(court, calendar_parser.CANDParser)


if __name__ == '__main__':
    unittest.main()
