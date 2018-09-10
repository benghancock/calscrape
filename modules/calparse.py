"""A module for parsing html from public court calendars"""

from datetime import datetime
import re

class ParsedCal():
    """A calendar parser object"""

    def __init__(self, raw):
        """Initialize parsed calendar's objects"""
        self.raw = raw 

    def cand_dates(self):
        """
        Load the raw body of a CAND calendar and get dates
        """
        self.courtdates = []
        cal_dateformat = r'\b\w.+\d+.201\d\b'

        for entry in self.raw:
            courtdate = re.search(cal_dateformat, entry)
        
            if courtdate:
                
                try:
                    fmt_courtdate = datetime.strptime(
                            courtdate.group(), '%A, %b %d %Y')
                    self.courtdates.append(fmt_courtdate)
               
                except ValueError:
                    pass

            else:
                continue

        return self.courtdates


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
