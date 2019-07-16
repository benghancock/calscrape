#!/usr/bin/env python3

# test_hearings.py

"""
Test functions in the hearings_diff module
"""

import json
import unittest
import hearings as hearings


class TestHearingsFunctions(unittest.TestCase):

    def setUp(self):
        # Bring in sample data to test hearing checkers
        test_data_file = "test_data/test_hearing_data.json"
        before_data_file = 'test_data/test_hearings_before.json'
        now_data_file = 'test_data/test_hearings_now.json'

        with open(test_data_file) as f:
            self.test_data = json.load(f)

        with open(before_data_file) as before_data_obj:
            self.before_data = json.load(before_data_obj)

        with open(now_data_file) as now_data_obj:
            self.now_data = json.load(now_data_obj)

    def test_restruct_hearings(self):
        # TODO Update with newer data sample including year timestamp
        restruct_data = hearings.restructure_hearing_data(
            self.test_data, key_name='case_no')

        case_nums = [case.get('case_no') for case in self.test_data]
        for key in restruct_data.keys():
            self.assertTrue(key in case_nums)

    def test_hearings_same(self):
        dict1 = {'name': 'Zero Cool', 'city': 'Seattle'}
        dict2 = {'name': 'Zero Cool', 'city': 'Seattle'}
        dict3 = {'name': 'Zero Cool', 'city': 'New York'}
        self.assertTrue(
            hearings.hearings_same(dict1, dict2, keys=['name', 'city']))
        self.assertFalse(
            hearings.hearings_same(dict1, dict3, keys=['name', 'city']))

    def test_time_past(self):
        t1 = "Tue Apr 23 2019 02:00 PM"
        t2 = "Fri Mar 17 2030 08:00 AM"

        self.assertTrue(hearings.time_past(t1))
        self.assertFalse(hearings.time_past(t2))

    def test_check_for_new(self):
        hearings_data = hearings.Hearings(latest_scrape=self.now_data,
                                          prior_scrape=self.before_data)

        new_hearings = hearings_data.check_for_new(keys=['judge',
                                                         'date',
                                                         'case_cap',
                                                         'detail'])

        new_caps = [h.get('case_cap') for h in new_hearings]
        self.assertTrue(len(new_hearings) == 1)
        self.assertTrue('USA v. Perry Gaines' in new_caps)
        self.assertFalse('Green v. Mercy Housing, Inc. et al' in new_caps)


if __name__ == '__main__':
    unittest.main()
