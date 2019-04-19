# hearings_diff.py

"""
Create Hearings class and associated methods
"""

class Hearings():
    """
    Model court hearings and introduce methods to detect
    differences between two JSON hearing files
    """

    def __init__(self, latest_scrape, prior_scrape):
        """Initialize attributes"""

        self.latest_scrape = latest_scrape
        self.prior_scrape = prior_scrape
