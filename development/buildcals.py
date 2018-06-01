#! /usr/bin/env python3

from lxml import html
import re, requests

class CourtCal():
    """A class for extracting data from an online court calendar"""

    def __init__(self, calurl):
        """Initialize attributes"""
        self.calurl = calurl
        self.judge = ""
        self.dates = []
        self.keymatches = {}
        self.casematches = {}
    
    def getcal(self):
        """Download the calendar and load the contents""" 
        cal = requests.get(self.calurl)
        caltree = html.fromstring(cal.content)
        calcontent = caltree.xpath('//td/text()')
        return calcontent

    def getdates(self):
        """Get all dates on a calendar"""
        calbody = self.getcal()
        
        dateformat = r'\b\w.+\d+.201\d\b'
        for entry in calbody:
            date = re.search(dateformat, entry)

            if date:
                self.dates.append(date.group())

            else:
                continue

        return self.dates


    # def searchkeywords(self):
        #TODO

    # def searchcases(self):
        #TODO

url = 'https://www.cand.uscourts.gov/CEO/cfd.aspx?7144'

c = CourtCal(url)
t = c.getdates()

print(t)

