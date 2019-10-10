"""
A module for handling data about court hearings
"""


class Hearings():
    """Object for outputing and comparing hearing data"""

    def __init__(self, hearing_data, scrape_time):
        self.hearing_data = hearing_data
        self.scrape_time = scrape_time

