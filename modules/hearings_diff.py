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

def compare_times(t1, t2):
    """
    Compare two times given in string format

    Datetimes must be in format '%a %b %d %I:%M %p'
    (i.e. "Tue Apr 23 02:00 PM")

    Parameters
    ----------
    t1 : string, datetime in specified format
    t2 : string, datetime in specified format

    Returns
    -------
    timediff : difference as type datetime.timedelta

    """
    t1 = datetime.strptime(t1, '%a %b %d %I:%M %p')
    t2 = datetime.strptime(t2, '%a %b %d %I:%M %p')

    timediff = t1 - t2
    return timediff


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
        # TODO Check the current date and handle hearings that have passed

        for case_num in self.latest_scrape.keys():
            now_hearings = self.latest_scrape.get(case_num)
            before_hearings = self.prior_scrape.get(case_num)

            if not before_hearings:
                # If case number wasn't previously present
                # then all hearings with that case number are new
                # UNLESS the hearing date has already passed

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

    def check_status(self):
        """
        Check prior scrape against latest scrape to see whether
        a hearing has gone off calendar or has been changed
        """

        # TODO
