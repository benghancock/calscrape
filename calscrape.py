#!/usr/bin/env python3

"""CalScrape - A tool for searching federal court calendars

This is the main script for scraping and returning calendar data.
"""

from modules.spatula import Spatula
from modules.calparse import ParsedCal
import json

def greet_user(version, supported):
    """Greet the user and provide basic info about the program"""
    greeting = "\n\t#################"
    greeting += "\n\t##  CalScrape  ##"
    greeting += "\n\t#################"

    description = "A tool for rapidly searching judicial calendars."
    version_line = f"VERSION {version}"
    
    print(greeting)
    
    print("\n")
    print(description)
    print(version_line)
    
    print("\nThe following courts are currently supported:")

    for court in supported:
        print(court.upper())


def prompt_user(supported):
    """Prompt the user and check for supported calendars

    Expects list as arg
    """
    prompt = "\nEnter the code of the court to be searched. For example,"
    prompt += "\nenter \"CAND\" for the Northern District of California."
    prompt += "\nOr enter \"q\" to quit."
    print(prompt)

    prompting = True
    selection = None

    while prompting:
        
        selection = input("\nSelection >> ")
        
        if selection.lower() == "q": 
            selection = None
            prompting = False 

        elif selection.lower() in supported:
            # Make the value lowercase before returning
            selection = selection.lower()
            prompting = False

        else:
            print("Not a valid selection.")
       
    return selection 

def pick_mode():
    """Prompts for list-based or single keyword search mode"""
    prompt = "\nPlease pick a search mode."
    prompt += "\nEnter \"keyword\" for a single keyword search,"
    prompt += "\nor enter \"list\" for a list-based search."
    print(prompt)

    prompting = True
    mode = None

    while prompting:
        
        mode = input("\nMode >> ")

        if mode == "keyword":
            prompting = False

        elif mode == "list":
            prompting = False

        else:
            print("Not a valid mode selection.")
       
    return mode
    
def load_calfile(selection):
    """Load the calendars JSON file

    Expects arg `selection` as string
    """
    try: 
        with open(f"data/{selection}-urls.json") as f:
            calendars = json.load(f)
    
        return calendars

    except FileNotFoundError as e:
        print("No calendar file found for that court")
        print(f"Error: {e}")    

def read_results(results):
    """Parse list of dicts to cleanly ouput results of search"""
    for result in results:
        judge = result.get('judge')
        date = result.get('date')
        formatted_date = date.strftime('%a %b %d %I:%M %p')
        case = result.get('case')
        details = result.get('details')

        print(f"Judge: {judge}")
        print(f"Date: {formatted_date}")
        print(f"Case: {case}")
        print(f"Hearing: {details}")
        print("\n")

def main():
    """Print neatly formatted results of calendar search"""
    version = "1.0" 
    # Set the supported calendars
    supported = ['cand']

    greet_user(version=version, supported=supported)

    # Set a run flag
    running = True
    
    while running:
        
        selection = prompt_user(supported)
        
        if selection == "cand":
            calfile = load_calfile(selection)
            
            if calfile == None:
                running = False

            else:
                
                mode = pick_mode()
                results = []

                if mode == "keyword":
                    searchterm = input("\nKeyword: ")
                    
                    print("Searching ...")

                    for judge, url in calfile.items():
                        page = Spatula(url)
                        page.scrape()
                        raw = page.serve_cand()

                        cal = ParsedCal(raw)
                        matches = cal.cand_search(searchterm, judge)
                        
                        # Test whether list is empty
                        if not matches:
                            pass
                        
                        else:
                            for match in matches:
                                results.append(match)

                elif mode == "list":
                    # Dummy list for testing
                    searchterms = ['google', 'facebook', 'pacific gas']

                    print("Searching ...")

                    for judge, url in calfile.items():
                            page = Spatula(url)
                            page.scrape()
                            raw = page.serve_cand()

                            cal = ParsedCal(raw)
                            
                            for searchterm in searchterms:
                                matches = cal.cand_search(searchterm, judge)
                                
                                # Test whether list is empty
                                if not matches:
                                    pass
                                
                                else:
                                    for match in matches:
                                        results.append(match)

                if not results:
                    print("No matches")

                else:
                    results_ordered = sorted(results, 
                            key = lambda k: k['date'])
                    read_results(results_ordered)
                
                running = False

        else:
            running = False


if __name__ == "__main__":
    main()

# # Import necessary modules
# from lxml import html
# import re, requests, json, sys
# 
# # Open the necessary calendar, search terms and cases files
# calfile = 'ndcal.json'
# keyfile = 'searchterms.json'
# casefile = 'cases.json'
# 
# 
# try:
#     with open (calfile) as f:
#         calendars = json.load(f)
# 
# except FileNotFoundError:
#     print("Court calendar file not found.")
#     sys.exit(1)
# 
# try:
#     with open(keyfile) as g:
#         searchkeys = json.load(g)
# 
# except FileNotFoundError:
#     print("Keyword case file not found.")
#     sys.exit(1)
# 
# try:
#     with open(casefile) as h:
#         cases = json.load(h)
# 
# except FileNotFoundError:
#     print("Cases file not found.")
#     sys.exit(1)
# 
# # Set keyword matches counters 
# word_matches = 0
# judge_matches = 0
# total_matches = 0
# 
# # Set case matches counter and default flag for cases
# case_matches = 0
# followed_cases = False
# 
# # Formula for dates while searching
# dateformat = r'\b\w.+\d+.201\d\b'
# 
# print("\n=== Search Results ===\n") 
# 
# # Loop through all calendars
# for judge, cal_url in calendars.items():
# 
# ## Check for good connection
#     try:
#         cal = requests.get(cal_url)
#          
#     except requests.exceptions.RequestException as e:
#         print("*** Connection problem. Please check internet connection ***")
#         print("\nReceived following error: ")
#         print(e)
#         sys.exit(1)
# 
#     print("\n\t>>> Judge " + judge.upper() + ":")
#     
#     # Build a list with all the entries on the calendar 
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
# 
#         if word_matches > 0:
#             
#             # Print the results, neatly formatted
#             print(str(word_matches) + " matches for \"" + keyword + "\"\n")
#             # Reset match counter to 0
#             word_matches = 0 
# 
#         else:
#             continue
#   
#     if judge_matches == 0:
#         print("No keyword search matches")
# 
#     else:
#         judge_matches = 0
# 
#     # Search for cases of interest
#     for casejudge, casenums in cases.items():
#         
#         # Only search calendar if the case is front of this judge
#         if casejudge == judge:
#         
#             # Set a flag indicating casenums followed on judge's calendar
#             followed_cases = True
# 
#             for casenum in casenums:
#                 searchcase = r'\b' + casenum + r'-\w+\b'
# 
#                 for entry in content:
#                     casedate = re.search(dateformat, entry)
#                     casematch = re.search(searchcase, entry, re.IGNORECASE)
#                                
#                     # Grab hearing dates while scanning; print only if match
#                     if casedate:
#                         currentcasedate = casedate
# 
#                     elif casematch:
#                         case_matches += 1
#                         print(currentcasedate.group())
#                         print("FOLLOWED CASE: " + entry)
# 
#                         # Get hearing information in next entry and print
#                         caseindex = content.index(entry) + 1
#                         print(content[caseindex])
# 
#                     else:
#                         continue
# 
#                 if case_matches == 0:
#                     print("No case number matches")
#                     
#                 else:
#                     case_matches = 0
#                     pass
# 
#         else:
#             continue
# 
#     if followed_cases == False: 
#         print("No case numbers followed on this calendar.")
# 
#     else:
#         followed_cases = False # Reset flag
#         
# 
# print("\n=== Search Complete ===")
# 
# if total_matches == 0:
# 
#     print("No matches on any calendar")    
# 
# else:
# 
#     pass 
# 
