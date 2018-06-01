#! /usr/bin/env python3

# Import necessary modules
from lxml import html
import re, requests, json, sys

# Open the necessary calendar, search terms and cases files
calfile = 'ndcal.json'
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

# Set keyword matches counters 
word_matches = 0
judge_matches = 0
total_matches = 0

# Set case matches counter and default flag for cases
case_matches = 0
followed_cases = False

# Formula for dates while searching
dateformat = r'\b\w.+\d+.201\d\b'

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

        for entry in content:
            date = re.search(dateformat, entry)           
            match = re.search(current_key, entry, re.IGNORECASE)

            # Grab the dates while scanning; only print if keyword mathc
            if date:
                currentdate = date
            
            elif match:
                word_matches += 1
                judge_matches += 1
                total_matches += 1            
                print(currentdate.group())
                print(entry)
                
                # Get hearing information in next entry and print
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
        print("No keyword search matches")

    else:
        judge_matches = 0

    # Search for cases of interest
    for casejudge, casenums in cases.items():
        
        # Only search calendar if the case is front of this judge
        if casejudge == judge:
        
            # Set a flag indicating casenums followed on judge's calendar
            followed_cases = True

            for casenum in casenums:
                searchcase = r'\b' + casenum + r'-\w+\b'

                for entry in content:
                    casedate = re.search(dateformat, entry)
                    casematch = re.search(searchcase, entry, re.IGNORECASE)
                               
                    # Grab hearing dates while scanning; print only if match
                    if casedate:
                        currentcasedate = casedate

                    elif casematch:
                        case_matches += 1
                        print(currentcasedate.group())
                        print("FOLLOWED CASE: " + entry)

                        # Get hearing information in next entry and print
                        caseindex = content.index(entry) + 1
                        print(content[caseindex])

                    else:
                        continue

                if case_matches == 0:
                    print("No case number matches")
                    
                else:
                    case_matches = 0
                    pass

        else:
            continue

    if followed_cases == False: 
        print("No case numbers followed on this calendar.")

    else:
        followed_cases = False # Reset flag
        

print("\n=== Search Complete ===")

if total_matches == 0:

    print("No matches on any calendar")    

else:

    pass 

