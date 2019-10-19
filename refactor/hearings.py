"""
A module for handling data about court hearings
"""


class Hearings():
    """Object for outputing and comparing hearing data"""

    def __init__(self, hearing_data):
        self.hearing_data = hearing_data

    def detect_new(self, prior_scrape):
        """A method for detecting new hearings"""
        this_set = self.make_set(self.hearing_data)
        prior_set = self.make_set(prior_scrape)

        return this_set.difference(prior_set)
        
    def make_set(self, data):
        """Convert hearing data into set of tuples for comparison purposes"""
        hearings_set = set(
            tuple(sorted(h.items())) for h in data
            )

        return hearings_set

    def revert_list(self, set_data):
        """Revert a set of tuple elements back to a list of dictionaries"""
        list_data = []

        for elem in set_data:
            list_data.append(dict((k, v) for k, v in elem))

        return list_data
