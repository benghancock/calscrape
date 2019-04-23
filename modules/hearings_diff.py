# hearings_diff.py

"""
Create Hearings class and associated methods
"""

def restructure_hearing_data(data, key_name):
    """
    Transform list of hearing data to dict of lists, by 'key_name'
    """
    dict_data = {}

    for entry in data:
        key_val = entry.pop(key_name)
        dict_data[key_val] = []
        dict_data[key_val].append(entry)

    return dict_data


class Hearings():
    """
    Model court hearings and introduce methods to detect
    differences between two JSON hearing files
    """

    def __init__(self, latest_scrape, prior_scrape):
        """Initialize attributes"""

        self.latest_scrape = latest_scrape
        self.prior_scrape = prior_scrape


    def check_for_new(self):
        """
        Compare the data from the latest scrape against the prior
        scrape to determine which hearings are new
        """
        # TODO

    def check_status(self):
        """
        Check prior scrape against latest scrape to see whether
        a hearing has gone off calendar or has been changed
        """

        # TODO
