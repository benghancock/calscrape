
"""
A module for handling data about court hearings
"""

from datetime import datetime
import json


def load_hearings(scrape_file):
    """Return a Hearings object with locally stored scrape data"""
    with open(scrape_file) as f:
        scrape = json.load(f)

    hearing_data = scrape.get('hearing_data')
    scrape_ts_string = scrape.get('scrape_ts')

    # The datetime data needs to be reverted to a datetime object
    scrape_ts_dt = datetime.strptime(
            scrape_ts_string,
            '%Y-%m-%d %H:%M %z'
        )

    for hearing in hearing_data:
        hearing_ts_string = hearing.get('date')
        hearing_ts_dt = datetime.strptime(
            hearing_ts_string,
            '%Y-%m-%d %H:%M %z'
        )
        hearing['date'] = hearing_ts_dt

    return Hearings(hearing_data, scrape_ts_dt)


class Hearings():
    """Object for outputing and comparing hearing data"""

    def __init__(self, hearing_data, scrape_ts):
        self.hearing_data = hearing_data
        self.scrape_ts = scrape_ts

    def detect_new(self, prior_scrape):
        """Detect which hearings in the latest scrape are new

         1. Check each hearing in the latest scrape
        2. Is it the same as any of the hearings in the prior scrape?
        3. If no, then it's new
        """

        new_hearings = []

        for latest_hearing in self.hearing_data:
            if latest_hearing in prior_scrape.hearing_data:
                continue
            else:
                new_hearings.append(latest_hearing)

        return new_hearings

    def detect_cancelled(self, prior_scrape):
        """Return hearings that have been cancelled.

        This is intended to be invoked on the object representing the latest
        scrape. Hearings are determined to be cancelled if:

        1. They were present in the prior scrape and are not present
           in the latest scrape; AND
        2. They date of the hearing has not yet passed

        prior_scrape is assumed to be Hearings object

        """

        cancelled_hearings = []

        for prior_hearing in prior_scrape.hearing_data:
            if prior_hearing not in self.hearing_data:
                hearing_dt = prior_hearing.get('date')

                if hearing_dt > self.scrape_ts:
                    cancelled_hearings.append(prior_hearing)

                else:
                    continue

            else:
                continue

        return cancelled_hearings

    def store_scrape(self, target):
        """Store the scrape data on the local machine as JSON"""

        # Convert the scrape_ts to a string:
        ts_string = datetime.strftime(
            self.scrape_ts,
            '%Y-%m-%d %H:%M %z'
        )

        # Make a container for the data
        storage_container = {
            'scrape_ts': ts_string,
            'hearing_data': self.hearing_data
        }

        # Convert all the datetime data to string
        for entry in storage_container['hearing_data']:
            date_dict = {
                'date': datetime.strftime(
                    entry.get('date'),
                    '%Y-%m-%d %H:%M %z'
                )
            }

            entry.update(date_dict)

        with open(target, 'w') as f:
            json.dump(storage_container, f)
