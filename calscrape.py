#! /usr/bin/env python3
# Python web scraping project for federal judicial calendars 
# Ben Hancock. v0.1: in development / no license

# Import necessary modules
from lxml import html
import re, requests, json, sys

# Open the local calendar file // NDCAL ONLY SO FAR
calfile = 'ndcal_test.json'

try:
    with open (calfile) as f:
        calendars = json.load(f)

except FileNotFoundError:
    print("Court calendar file not found.")
    sys.exit(1)

# Open search terms file 
keyfile = 'searchterms.json'

try:
    with open(keyfile) as g:
        searchkeys = json.load(g)

except FileNotFoundError:
    print("Keyword search file not found.")
    sys.exit(1)


# Set a variable for number of matches
matches = 0
total_matches = 0

print("\n=== Keyword search results ===\n") 
# Loop through all calendars
for judge, cal_url in calendars.items():

## Check for good connection
    try:
        cal = requests.get(cal_url)
    
    except requests.exceptions.RequestException as e:
        print("Connection problem: " + e)
        sys.exit(1)

    print("Results for Judge " + judge.upper() + ":")
    
    tree = html.fromstring(cal.content)
    content = tree.xpath('//td/text()')

    # Build a list with all the entries on the website

    for keyword in searchkeys:
        
        current_key = r'\b' + keyword + r'\b' 

        # Loop through the contents searching for the calendar
        for entry in content:
            match = re.search(current_key, entry, re.IGNORECASE)
            
            if match:
                matches += 1
                total_matches += 1            

            else:
                continue

        if matches > 0:
            
            # Print the results, neatly formatted
            print(str(matches) + " matches for \"" + keyword + "\"")
            # Reset match counter to 0
            matches = 0 

        else:

            continue

print("\n=== Search complete ===")

if total_matches == 0:

    print("No matches on any calendar")    

else:

    pass 

