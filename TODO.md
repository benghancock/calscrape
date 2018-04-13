# ROADMAP for Calscrape project

## Phases

## V0.1
SPEC: Searches a list of calendars for given keywords and/or case numbers,
tells user if keyword or num is found and on which judge's calendar.

TODO (Unorderred):
* [DONE] Implement search for keywords using 'for' loops and regex
* Build .json files with addresses and keywords to search
    * Rebuild loop structures to handle searching of each site, keyword
* Error handling for connection failure and other exceptions
* Implement progress bar during search
* Handle not found result
* Use version control
* Host code on Github

## V0.2
SPEC: Searches for keywords and/or case numbers, serves up to user NAME of
judge on whose calendar it appears, as well as DATE and TIME

## V0.3 
SPEC: Implements above, but RUNS automatically at given time every day/week and
sends data to a user.

