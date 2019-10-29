
"""
A module for handling data about court hearings
"""

from datetime import datetime
import json


def load_hearings(scrape_file):
    """Return a Hearings object with locally stored scrape data"""
    with open(scrape_file) as f:
        scrape = json.load(f)

    hearing_data = scrape.get('data')
    store_ts = scrape.get('store_ts')

    return Hearings(hearing_data, store_ts)


class Hearings():
    """Object for outputing and comparing hearing data"""

    def __init__(self, hearing_data, store_ts=''):
        self.hearing_data = hearing_data
        self.store_ts = store_ts

    def detect_new(self, prior_scrape):
        """A method for detecting new hearings"""
        this_set = self.make_set(self.hearing_data)
        prior_set = self.make_set(prior_scrape)

        new = this_set.difference(prior_set)
        new_reverted = self.revert_list(new)

        return new_reverted

    def detect_cancelled(self, prior_scrape, scrape_time):
        """Return hearings that have been cancelled

        Hearings are determined to be cancelled if:
        1. They were present in the prior scrape and are not present
           in the latest scrape; AND
        2. They date of the hearing has not yet passed

        prior_scrape is assumed to be Hearings object
        """
        prior = self.make_set(prior_scrape.hearing_data)
        latest = self.make_set(self.hearing_data)

        absent_set = prior.difference(latest)
        absent_hearings = self.revert_list(absent_set)

        cancelled_hearings = []

        for hearing in absent_hearings:
            # date should be datetime object
            hearing_dt = hearing.get('date')

            # was the hearing scheduled for a future date?
            # or is it absent because the date has passed?
            if hearing_dt > scrape_time:
                cancelled_hearings.append(hearing)
            else:
                continue

        return cancelled_hearings

    def make_set(self, data):
        """Convert list of dicts into set of tuples for comparison purposes"""
        set_data = set(
            tuple(sorted(h.items())) for h in data
            )

        return set_data

    def revert_list(self, set_data):
        """Revert a set of tuple elements back to a list of dicts"""
        list_data = []

        for elem in set_data:
            list_data.append(dict((k, v) for k, v in elem))

        return list_data

    def store_scrape(self, target):
        """Store the scrape data on the local machine as JSON"""

        # TODO Get timezone info from the local machine
        # make a copy
        storage_container = {
            'store_ts': datetime.strftime(
                datetime.now(),
                '%Y-%m-%d %H:%M %z'
                ),
            'data': self.hearing_data
            }

        # Convert all the datetime data to string
        for entry in storage_container.get('data'):
            date_dict = {
                'date': datetime.strftime(
                    entry.get('date'),
                    '%Y-%m-%d %H:%M %z'
                )
            }

            entry.update(date_dict)

        with open(target, 'w') as f:
            json.dump(storage_container, f)
