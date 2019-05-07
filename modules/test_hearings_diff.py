#!/usr/bin/env python3

# test_hearings_diff.py

"""
Test functions in the hearings_diff module
"""

import json
import unittest
import hearings_diff as hd

TEST_HEARINGS_DATA = [{"judge": "Alsup, William H. [WHA]",
                       "date": "Tue Apr 23 10:00 AM",
                       "case_no": "3:18-cv-04888-WHA",
                       "case_cap": "Green v. Mercy Housing, Inc. et al",
                       "detail": "Discovery Hearing"}]


class TestHearingsFunctions(unittest.TestCase):

    def setUp(self):
        # Bring in sample data to test hearing checkers
        before_data_file = 'test_hearings_before.json'
        now_data_file = 'test_hearings_now.json'

        with open(before_data_file) as bd_obj:
            self.before_data = json.load(bd_obj)

        with open(now_data_file) as nd_obj:
            self.now_data = json.load(nd_obj)


    def test_restruct_hearings(self):
       restruct_data = hd.restructure_hearing_data(TEST_HEARINGS_DATA, key_name='case_no')
       self.assertEqual(list(restruct_data.keys())[0], "3:18-cv-04888-WHA")
       self.assertEqual(restruct_data.get('3:18-cv-04888-WHA')[0].get('judge'),
                        "Alsup, William H. [WHA]")


    def test_hearings_same(self):
        dict1 = {'name': 'Zero Cool', 'city': 'Seattle'}
        dict2 = {'name': 'Zero Cool', 'city': 'Seattle'}
        dict3 = {'name': 'Zero Cool', 'city': 'New York'}
        self.assertTrue(hd.hearings_same(dict1, dict2, keys=['name', 'city']))
        self.assertFalse(hd.hearings_same(dict1, dict3, keys=['name', 'city']))


    def test_time_past(self):
        t1 = "Tue Apr 23 2019 02:00 PM"
        t2 = "Fri Mar 17 2030 08:00 AM"

        self.assertTrue(hd.time_past(t1))
        self.assertFalse(hd.time_past(t2))


    def test_check_for_new(self):


if __name__ == '__main__':
    unittest.main()

