"""A module for parsing html from public court calendars"""

from datetime import datetime
import re
import pandas as pd

class ParsedCal():
    """A calendar parser object"""

    def __init__(self, raw):
        """Initialize parsed calendar's objects"""
        self.raw = raw

    def cand_getalldates(self):
        """
        Load the raw body of a CAND calendar and get dates
        """
        self.courtdates = []
        cal_dateformat = r'\b\w.+\d+.201\d\b'

        for entry in self.raw:
            courtdate = re.search(cal_dateformat, entry)
        
            if courtdate:
                try:
                    formatted_courtdate = datetime.strptime(
                            courtdate.group(), '%A, %b %d %Y')
                    self.courtdates.append(formatted_courtdate)
               
                except ValueError:
                    pass

            else:
                continue

        return self.courtdates

    def cand_formatdate(self, rawdate):
        """Return a datetime formatted date"""
        formatted_courtdate = datetime.strptime(rawdate, '%A, %b %d %Y').date()
        return formatted_courtdate

    def cand_formattime(self, rawtime):
        """Return a datetime formatted time"""
        formatted_courttime = datetime.strptime(rawtime, '%I:%M%p').time()
        return formatted_courttime
        
    def cand_search(self, searchterm):
        """Return a pandas dataframe with matching calendar entries"""
        cal_dateformat = r'\b\w.+\d+.201\d\b'
        cal_timepattern = r'\d+:\d+\w+(AM|PM)'
        cal_searchpattern = r'\b' + searchterm + r'\b'

        # Create lists to hold the data series
        dates = []
        captions = []
        details = []

        for entry in self.raw:
            courtdate = re.search(cal_dateformat, entry)
            courttime = re.search(cal_timepattern, entry) 
            match = re.search(cal_searchpattern, entry, re.IGNORECASE)

            if courtdate:
                try:
                    current_courtdate = self.cand_formatdate(courtdate.group())

                except ValueError:
                    pass

            if courttime:
                try:
                    current_courttime = self.cand_formattime(courttime.group())

                except ValueError:
                    pass
            
            if match:
                dateinfo = datetime.combine(current_courtdate, 
                        current_courttime)
                dates.append(dateinfo)
                
                caption = entry 
                captions.append(caption)

                # Details of hearing are at next index location in list
                details_index = self.raw.index(entry) + 1
                caption_details = self.raw[details_index]
                details.append(caption_details)

            else:
                continue

        matches_df = pd.DataFrame({
            'date': dates,
            'captions': captions,
            'details': details
            })
        matches_df.set_index('date', inplace=True)
        
        return matches_df
