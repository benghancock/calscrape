"""A module for parsing html from public court calendars"""

from datetime import datetime
import re

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
        """Return a list of calendar items matching search term"""
        results = []
        cal_dateformat = r'\b\w.+\d+.201\d\b'
        cal_timepattern = r'\d+:\d+\w+(AM|PM)'
        cal_searchpattern = r'\b' + searchterm + r'\b'

        for entry in self.raw:
            courtdate = re.search(cal_dateformat, entry)
            courttime = re.search(cal_timepattern, entry) 
            match = re.search(cal_searchpattern, entry, re.IGNORECASE)
            result = ''

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
                match_text = match.group()
                dateinfo = datetime.combine(current_courtdate,
                        current_courttime)
                clean_date = datetime.strftime(dateinfo, '%a %b %Y %I:%M %P')

                result = f'{clean_date}\t{match_text}'
                results.append(result)

            else:
                continue

        return results
        


# calcontent = caltree.xpath('//td/text()')
# 
# # Build a list with all the entries on the calendar 
#     tree = html.fromstring(cal.content)
#     content = tree.xpath('//td/text()')
# 
#     # Search the list for desired keywords
#     for keyword in searchkeys:
#         current_key = r'\b' + keyword + r'\b' 
# 
#         for entry in content:
#             date = re.search(dateformat, entry)           
#             match = re.search(current_key, entry, re.IGNORECASE)
# 
#             # Grab the dates while scanning; only print if keyword mathc
#             if date:
#                 currentdate = date
#             
#             elif match:
#                 word_matches += 1
#                 judge_matches += 1
#                 total_matches += 1            
#                 print(currentdate.group())
#                 print(entry)
#                 
#                 # Get hearing information in next entry and print
#                 hearing_index = content.index(entry) + 1
#                 print(content[hearing_index])
# 
#             else:
#                 continue
