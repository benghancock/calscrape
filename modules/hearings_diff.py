# hearings_diff.py

"""
Create Hearings class and associated methods
"""

from datetime import datetime


def restructure_hearing_data(data, key_name):
    """
    Transform list of hearing data to dict of lists, by 'key_name'
    """
    dict_data = {}

    for entry in data:
        key_val = entry.get(key_name)

        # Don't overwrite if it's already been added
        if dict_data.get(key_val):
            dict_data[key_val].append(entry)

        else:
            dict_data[key_val] = []
            dict_data[key_val].append(entry)

    return dict_data


def hearings_same(data_1, data_2, keys):
    """
    Compare two dictionaries with hearing data
    If different, return False; else return True

    :keys: list of keys to compare
    """
    for key in keys:
        data_1_val = data_1.get(key)
        data_2_val = data_2.get(key)

        if data_1_val != data_2_val:
            return False

        else:
            continue

    return True


def time_past(timestamp):
    """Evaluate timestamp and return whether time is in the past

    ``timestamp`` must be in format '%a %b %d %Y %I:%M %p'
    (i.e. "Tue Apr 23 2019 02:00 PM")
    # TODO Change format

    :param timestamp: datetime in specified format
    :type timestamp: str

    :returns: whether timestamp is in the past
    :rtype: bool

    """

    timestamp = datetime.strptime(timestamp, '%a %b %d %Y %I:%M %p')
    now = datetime.now()

    time_past = now > timestamp
    return time_past


class Hearings():
    """
    Model court hearings and introduce methods to detect
    differences between two JSON hearing files
    """

    def __init__(self, latest_scrape, prior_scrape):
        """Initialize attributes"""

        self.latest_scrape = latest_scrape
        self.prior_scrape = prior_scrape

    def check_for_new(self, keys):
        """
        Compare the data from the latest scrape against the prior
        scrape to determine which hearings are new
        """
        new_hearings = []

        # Loop through every item in the latest scrape
        # and check for its existence in the prior scrape

        for case_num in self.latest_scrape.keys():
            now_hearings = self.latest_scrape.get(case_num)
            before_hearings = self.prior_scrape.get(case_num)

            # if case number wasn't previously present
            # then all hearings with that case number are new
            # unless the hearing date has already passed
            if not before_hearings:

                for now_hearing in now_hearings:
                    new_hearings.append(now_hearing)

            else:
                for now_hearing in now_hearings:
                    for before_hearing in before_hearings:
                        if hearings_same(now_hearing, before_hearing, keys):
                            continue
                        else:
                            new_hearings.append(now_hearing)

        return new_hearings

    def check_status(self, keys):
        """
        Check prior scrape against latest scrape to see whether
        a hearing has gone off calendar or has been changed
        """

        canceled_hearings = []

        for case_num in self.prior_scrape.keys():
            before_hearings = self.prior_scrape.get(case_num)
            now_hearings = self.latest_scrape.get(case_num)

            # Has the date past?
            for before_hearing in before_hearings:
                hearing_date = before_hearing.get('date')

                # If the date is in the past, do nothing
                if time_past(hearing_date):
                    continue

                else:
                    # If no matching case numbers, hearing is canceled
                    if not now_hearings:
                        canceled_hearings.append(before_hearing)

                    else:
                        for now_hearing in now_hearings:
                            if hearings_same(before_hearing, now_hearing, keys):
                                continue
                            else:
                                canceled_hearings.append(before_hearing)
