#! /usr/bin/env python3
# Configure CalScrape search keywords and tracked cases

import json

keywordfile = 'searchterms.json'
casesfile = 'cases.json'

def createsearchlist():
    """Create a list of keywords to search on the calendar"""
    prompt = "Enter desired search terms, separated by commas, then hit enter:"
    userterms = input(prompt + "\n")
    termslist = [term.lstrip().lower() for term in userterms.split(',')]
    
    with open(keywordfile, 'w') as f:
        json.dump(termslist, f)

def readsearchlist():
    """Read and print a list of current search terms"""
    
    try:
        with open(keywordfile) as f:
            searchterms = json.load(f)

        print("=== CURRENT SEARCH TERMS ===")

        for term in searchterms:
            print(term)

        return True

    except json.decoder.JSONDecodeError:
        print("Problem with your search file.")
        return False

def addsearchterms():
    """Add search terms to an existing list"""
    prompting = True
    prompt = "\nWould you like to add more search terms? (Y/n) "
    
    while prompting:
        addstatus = input(prompt)

        if addstatus == "Y":
            
            try:
                addprompt = "Enter desired search terms, separated by commas, then hit enter:"
                userterms = input(addprompt + "\n")
                newtermslist = [term.lstrip().lower() for term in userterms.split(',')]
                
                with open(keywordfile) as f:
                    searchterms = json.load(f)

                for term in newtermslist:
                    searchterms.append(term)
                
                with open(keywordfile, 'w') as f:
                    json.dump(searchterms, f)
                
                print("Done.")
            
            except json.decoder.JSONDecodeError:
                print("Problem with your search file.")

        elif addstatus == "n":
            print("Done.")
            prompting = False

        else:
            print("Invalid option.")
            continue


while True:

    try:
        if readsearchlist():
            addsearchterms()
            break

        else:
            break
            
    except FileNotFoundError:
        createsearchlist()
        readsearchlist()
        addsearchterms()
        break
