"""
Select the correct parser for a given court
"""

import configparser
import modules.calendar_parser as calparse


def select_court(court_code):
    """Returns CalendarParser object"""

    config = configparser.ConfigParser()
    config.read('calendars_conf.ini')

    if court_code == 'cand':
        parser = calparse.CANDParser(config['CAND']['CAND_BASEURL'],
                                     config['CAND']['CAND_INDEX'])
        return parser

    else:
        return None
