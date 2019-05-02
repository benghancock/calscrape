#!/usr/bin/env python3

"""Unit tests for Calscrape functions"""

from datetime import datetime
import unittest
import calscrape

class TestFormattingFuncs(unittest.TestCase):
    """Tests functions to reformat and reorder data in `calscrape.py`."""

    def test_reformat_date(self):
        """Test that datetime objs are formatted as strings correctly"""
        example_hearing = {'judge': 'Alsup, William H. [WHA]',
                           'date': datetime(2019, 2, 14, 8, 0),
                           'case_no': '3:18-cv-06113-WHA', 
                           'case_cap': 'Howard Clark, et al  v. The Hershey Company'} 
        example_date_string = "Thu Feb 14 2019 08:00 AM"

        calscrape.reformat_date(example_hearing)
        reformatted_date = example_hearing.get('date')

        self.assertEqual(reformatted_date, example_date_string)

unittest.main()        
