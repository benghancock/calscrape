#! /usr/bin/env python3
# Configure CalScrape search keywords and tracked cases

import json

keywordfile = 'searchterms.json'
casesfile = 'cases.json'

def createsearchlist():
    """Create a list of keywords to search on the calendar"""
    prompt = "Enter desired search terms, separated by commas, then hit enter:"
    userterms = input(prompt + "\n")
    termslist = [term.lstrip().lower() for term in userterms.split()]
    
    with open(keywordfile, 'w') as f:
        json.dump(termslist, f)

def readsearchlist():
    """Read and print a list of current search terms"""
    with open(keywordfile) as f:
        searchterms = json.load(f)

    print("=== CURRENT SEARCH TERMS ===")

    for term in searchterms:
        print(term)

def addsearchterms():
   """Add search terms to an existing list"""
   #TODO 

while True:
    try:
        readsearchlist()
        break
            
    except FileNotFoundError:
        createsearchlist()
        break
