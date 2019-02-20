#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for Calscrape.'''

import betamax
import pytest

from calscrape import courts

pytest.mark.usefixtures('betamax_session')


class TestEDTX():
    '''Test EDTX calendar parser.'''
    @pytest.fixture(autouse=True)
    def _parser(self):
        '''Create parser fixture.'''
        self.parser = courts.edtx

    def test_parse_stored_session(self):
        '''Unit test using stored request data.'''
        recorder = betamax.Betamax(self.parser.session)
        with recorder.use_cassette('edtx_session'):
            assert self.parser.calendar
            assert len(self.parser.calendar) == 138
            expected_keys = ['judge name', 'url', 'docket no.', 'inst no.',
                             'party', 'hearing type', 'timestamp']
            assert expected_keys == list(self.parser.calendar[0])

    @pytest.mark.slow
    def test_edtx_parse(self):
        '''Functional test using network connection.'''
        self.parser.parse_court_calendar()
        assert self.parser.calendar
