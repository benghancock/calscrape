#! /usr/bin/env python3
# Python web scraping project for federal judicial calendars 
# Ben Hancock. In development / No license

# Import necessary modules
from lxml import html
import re
import requests

# Get the webpage and build the html 'tree'
cal = requests.get('https://www.cand.uscourts.gov/CEO/cfd.aspx?7134')
tree = html.fromstring(cal.content)

# Build a list with all the entries on the website
content = tree.xpath('//td/text()')

# Pull courtroom and get judge's name
courtroom = tree.xpath('//a[@name="#top"]/strong/text()')
judge = re.search(r'\bJudge\s\w+\s\w+.\s\w+\b', courtroom[0])

# Test key and create regex search key
key = 'Hussain'
searchkey = r'\b' + key + r'\b'

# Set a variable for number of matches
matches = 0

# Loop through the contents searching for the calendar
for entry in content:
    match = re.search(key, entry, re.IGNORECASE) 
    
    if match:
        matches += 1

    else:
        continue

# Print the results, neatly formatted
print(str(matches) + ' matches found for ' + key + ' in the following courtroom:')
print(judge.group()) 
