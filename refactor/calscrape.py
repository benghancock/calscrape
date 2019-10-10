#!/usr/bin/env python3

"""
CalScrape: rapidly scrape and search judicial calendars
"""

import configparser

import calendar_parser

COURTS_CONFIG = "courts_config.ini"


def load_courts_config(config_file):
    """Load hard-coded configurations"""
    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def select_court(court_string, config):
    """Return an instance of the correct court parser based on arg"""

    # California Northern District
    if court_string.lower() == 'cand':
        parser = calendar_parser.CANDParser(config['CAND']['CAND_BASEURL'],
                                            config['CAND']['CAND_INDEX'])
        return parser

    else:
        return None
