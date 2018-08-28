# spatula: a module for extracting judicial calendars from court websites

from lxml import html

    def getcal(self):
        """Download the calendar and load the contents""" 
        cal = requests.get(self.calurl)
        caltree = html.fromstring(cal.content)
        calcontent = caltree.xpath('//td/text()')
        return calcontent


