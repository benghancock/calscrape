#!/usr/bin/env python 3

"""
Tests for calscrape.py and modules
"""

import configparser
import unittest

import calscrape
import calendar_parser

COURTS_CONFIG = 'courts_config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(COURTS_CONFIG)


class TestCalscrape(unittest.TestCase):

    def test_select_court(self):
        test_court = "CAND"
        court = calscrape.select_court(test_court, CONFIG)
        self.assertIsInstance(court, calendar_parser.CANDParser)


if __name__ == '__main__':
    unittest.main()
