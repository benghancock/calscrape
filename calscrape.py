#! /usr/bin/env python3
# Python web scraping project for federal judicial calendars 
# Ben Hancock. v0.1: in development / no license

# Import necessary modules
from lxml import html
import re, requests, json

try:
    court = input("Court: ")
    filename = court.lower() + ".json"

    with open (filename) as f:
        calendars = json.load(f)

except FileNotFoundError:
    print("Court file for " + court + " not found.")

# Get search term
key = input("Search term: ")

# Set a variable for number of matches
matches = 0
total_matches = 0


print("\n=== Results for term \"" + key + "\" on calendars ===")
# Loop through all calendars
for judge, cal_url in calendars.items():

    # Get the webpage and build the html 'tree'
    cal = requests.get(cal_url)
    tree = html.fromstring(cal.content)

    # Build a list with all the entries on the website
    content = tree.xpath('//td/text()')

   # Test key and create regex search key
    searchkey = r'\b' + key + r'\b'

    # Loop through the contents searching for the calendar
    for entry in content:
        match = re.search(searchkey, entry, re.IGNORECASE) 
        
        if match:
            matches += 1
            total_matches += 1            

        else:
            continue

    if matches > 0:
        
        # Print the results, neatly formatted
        print("Judge " + judge.upper() + ": " + str(matches) + " matches.")       
        # Reset match counter to 0
        matches = 0 

    else:

        continue

print("Search complete")

if total_matches == 0:

    print("No matches on any calendar")    

else:

    pass 

