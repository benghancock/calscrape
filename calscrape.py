#! /usr/bin/env python3

# Import necessary modules
from lxml import html
import re, requests, json, sys

# Open the necessary calendar, search terms and cases files
calfile = 'ndcal_test.json'
keyfile = 'searchterms.json'
casefile = 'cases.json'

try:
    with open (calfile) as f:
        calendars = json.load(f)

except FileNotFoundError:
    print("Court calendar file not found.")
    sys.exit(1)

try:
    with open(keyfile) as g:
        searchkeys = json.load(g)

except FileNotFoundError:
    print("Keyword case file not found.")
    sys.exit(1)

try:
    with open(casefile) as h:
        cases = json.load(h)

except FileNotFoundError:
    print("Cases file not found.")
    sys.exit(1)

####################################

# Set a variable for number of matches
word_matches = 0
judge_matches = 0
total_matches = 0

print("\n=== Search Results ===\n") 

# Loop through all calendars
for judge, cal_url in calendars.items():

## Check for good connection
    try:
        cal = requests.get(cal_url)
         
    except requests.exceptions.RequestException as e:
        print("*** Connection problem. Please check internet connection ***")
        print("\nReceived following error: ")
        print(e)
        sys.exit(1)

    print("\n\t>>> Judge " + judge.upper() + ":")
    
    # Build a list with all the entries on the calendar 
    tree = html.fromstring(cal.content)
    content = tree.xpath('//td/text()')

    # Search the list for desired keywords
    for keyword in searchkeys:
        current_key = r'\b' + keyword + r'\b' 
        dateformat = r'\b\w.+\d+.201\d\b'

        for entry in content:
            date = re.search(dateformat, entry)           
            match = re.search(current_key, entry, re.IGNORECASE)

            if date:
                currentdate = date
            
            elif match:
                word_matches += 1
                judge_matches += 1
                total_matches += 1            
                print(currentdate.group())
                print(entry)
                hearing_index = content.index(entry) + 1
                print(content[hearing_index])

            else:
                continue

        if word_matches > 0:
            
            # Print the results, neatly formatted
            print(str(word_matches) + " matches for \"" + keyword + "\"\n")
            # Reset match counter to 0
            word_matches = 0 

        else:
            continue
  
    if judge_matches == 0:
        print("None")

    else:
        judge_matches = 0
        continue

   
    # Search for cases of interest
    for casejudge, casenums in cases.items():

        if casejudge = judge:
            
            for casenum in casenums:
                searchcase = r'\b' + casenum + "-" + casejudge + r'\b'
                
                for entry in content:
                    match = re.search(searchcase, entry, re.IGNORECASE)
                    date = re.search(dateformat, entry)
                               
                    if date:
                        currentdate = date

                    elif match:
                        #TODO Define vars for counting; print case info

                    else:
                        continue

   print("\n=== Search Complete ===")

if total_matches == 0:

    print("No matches on any calendar")    

else:

    pass 

