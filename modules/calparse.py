"""A module for parsing html from public court calendars"""

from datetime import datetime
import re


class ParsedCal():
    """A calendar parser object"""

    def __init__(self, raw):
        """Initialize parsed calendar's objects"""
        self.raw = raw
        self.courtdates = []
        self.time_format = '%I:%M%p'
        self.date_format = '%A, %b %d %Y'
        self.cal_dateformat = r'\b\w.+\d+.201\d\b'
        self.cal_timepattern = r'\d+:\d+\w+(AM|PM)'

    def cand_getalldates(self):
        """
        Load the raw body of a CAND calendar and get dates
        """

        for entry in self.raw:
            courtdate = re.search(self.cal_dateformat, entry)

            if courtdate:
                try:
                    formatted_courtdate = datetime.strptime(
                        courtdate.group(), self.date_format)
                    self.courtdates.append(formatted_courtdate)

                except ValueError:
                    pass

            else:
                continue

        return self.courtdates

    def cand_search(self, searchterm, judge):
        """Return a list of dicts with matching calendar entries"""
        cal_searchpattern = r'\b' + searchterm + r'\b'

        results = []

        for entry in self.raw:
            courtdate = re.search(self.cal_dateformat, entry)
            courttime = re.search(self.cal_timepattern, entry)
            match = re.search(cal_searchpattern, entry, re.IGNORECASE)

            if courtdate:
                try:
                    current_courtdate = datetime.strptime(courtdate.group(),
                                                          self.date_format).date()

                except ValueError:
                    pass

            if courttime:
                try:
                    current_courttime = datetime.strptime(courttime.group(),
                                                          self.time_format).time()

                except ValueError:
                    pass

            if match:

                dateinfo = datetime.combine(current_courtdate,
                                            current_courttime)
                # Details of hearing are at next index location in list
                caption_details = self.raw[self.raw.index(entry) + 1]

                result = {'judge': judge,
                          'date': dateinfo,
                          'case': entry,
                          'details': caption_details}

                results.append(result)

            else:
                continue

        return results
