#! /usr/bin/env python3
# Python web scraping project for federal judicial calendars 
# Ben Hancock. v0.1: in development / no license

# Import necessary modules
from lxml import html
import re, requests, json

# Get search term
key = input("Search term: ")
filename = 'ndcal_cals.json'

# Set a variable for number of matches
matches = 0

with open (filename) as f:
    calendars = json.load(f)

# Loop through all calendars
for calendar in calendars:

    # Get the webpage and build the html 'tree'
    cal = requests.get(calendar)
    tree = html.fromstring(cal.content)

    # Build a list with all the entries on the website
    content = tree.xpath('//td/text()')

    # Pull courtroom and get judge's name
    courtroom = tree.xpath('//a[@name="#top"]/strong/text()')
    judge = re.search(r'\b(Calendar for\:.)(\w+.+\w+)\b', courtroom[0])
    # Test key and create regex search key
    searchkey = r'\b' + key + r'\b'

    # Loop through the contents searching for the calendar
    for entry in content:
        match = re.search(searchkey, entry, re.IGNORECASE) 
        
        if match:
            matches += 1

        else:
            continue

    if matches > 0:
        
        # Print the results, neatly formatted
        print(str(matches) + ' matches found for ' + key + ' in the following courtroom:')
        print(judge.group(2)) 
        matches = 0 # Reset match counter to 0

    else:

        continue

if matches == 0:
    
    print("No matches on any calendar")    

else:

    pass 

