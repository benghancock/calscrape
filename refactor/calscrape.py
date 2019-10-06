#!/usr/bin/env python3

"""
CalScrape: rapidly search and scrape juidical calendars
"""

import configparser

import calendar_parser

COURTS_CONFIG = 'courts_config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(COURTS_CONFIG)


def select_court(court_string, config):
    """Return an instance of the correct court parser based on arg"""

    # California Northern District
    if court_string.lower() == 'cand':
        parser = calendar_parser.CANDParser(config['CAND']['CAND_BASEURL'],
                                            config['CAND']['CAND_INDEX'])
        return parser

    else:
        return None
