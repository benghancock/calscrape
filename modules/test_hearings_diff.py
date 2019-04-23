#!/usr/bin/env python3

# test_hearings_diff.py

"""
Test functions in the hearings_diff module
"""

import unittest
import hearings_diff as hd

TEST_HEARINGS_DATA = [{"judge": "Alsup, William H. [WHA]",
                       "date": "Tue Apr 23 10:00 AM",
                       "case_no": "3:18-cv-04888-WHA",
                       "case_cap": "Green v. Mercy Housing, Inc. et al",
                       "detail": "Discovery Hearing"}]



class TestHearingsFunctions(unittest.TestCase):

    def test_restruct_hearings(self):
       restruct_data = hd.restructure_hearing_data(TEST_HEARINGS_DATA, key_name='case_no')
       self.assertEqual(list(restruct_data.keys())[0], "3:18-cv-04888-WHA")
       self.assertEqual(restruct_data.get('3:18-cv-04888-WHA')[0].get('judge'),
                        "Alsup, William H. [WHA]")


if __name__ == '__main__':
    unittest.main()

