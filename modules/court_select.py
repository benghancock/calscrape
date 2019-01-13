"""
Select the correct parser for a given court
"""

import modules.calendar_parser as calparse
import modules.calendarsconf as calconf


def select_court(court_code):
    """Returns CalendarParser object"""

    if court_code == 'cand':
        parser = calparse.CANDParser(calconf.CAND_BASEURL,
                                     calconf.CAND_INDEX)
        return parser

    else:
        return None
