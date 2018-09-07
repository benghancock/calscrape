"""A module for parsing html from public court calendars"""

class ParsedCal():
    """A calendar parser object"""

    def __init__(self, tree):
        """Initialize parsed calendar's objects"""
        self.tree = tree 
        self.raw = ''
        self.dates =  ''
        self.hearings = ''

    def cand_load(self):
        """
        Load the raw body of a CAND calendar
        Takes html tree as arg
        """
        self.raw = self.tree.xpath('//td/text()')
        return self.raw

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
