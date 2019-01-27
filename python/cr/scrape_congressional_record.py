"""Scrapes Senate congressional record. Input is: directory where to print the files start date: 01/01/2000 format, end date. End date defaults to current date if none given"""

import logging
import random
import re
import requests
import sys
from datetime import datetime, date, timedelta
from time import sleep

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

class NoCRContentException(Exception):
    """Raised when there is no CR content at the given url"""
    pass

class CRScraper:
    """Class for scraping one day's worth of content from the Congressional Record"""

    link_prefix = "https://www.congress.gov"

    def __init__(self, url, filename):
        self.url = url
        self.output_file = filename

    def get_links(self):
        """Gets links for one day of Congressional Record"""
        soup = BeautifulSoup(requests.get(self.url).content)
        links = [link for link in soup.find_all('td')]
        # Only even numbered indexes have the needed links
        relevant_links = [link[i].a.get('href') for i in range(len(links)) if i % 2 == 0]
        # Create full links if necessary
        return([self.link_prefix + l if re.match("^/", l) else l for l in relevant_links])

    def scrape_page(self, url):
        """Scrapes one section of the Congressional Record"""
        soup = BeautifulSoup(requests.get(url).content)
        text = soup.find('pre', class_ = 'styled').contents
        return(''.join(str(text)))

    def save_file(self):
        """Writes content to file"""
        log.info("Writing to file: " + self.filename)
        with open(self.filename, "w") as file:
            file.write(self.content)

    def run(self):
        """Scrapes one day of Congressional Record Content"""
        links = self.get_links()
        if len(links) == 0:
            raise NoCRContentException
        else:
            self.content = " ".join([self.scrape_page(url) for url in links])

class CRWriter:
    """Class for scraping and saving a complete time period of the Congressional Record"""
    max_pause = 4
    url_prefix = "https://www.congress.gov/congressional-record/"
    url_suffix_dict = {
            "s": "/senate-section",
            "h": "/house-section"}

    def __init__(self, house, directory, startdate, enddate):
        self.house = house.upper()
        self.url_suffix = self.url_suffix_dict[house]
        self.output_directory = directory
        self.startdate = datetime.strptime(startdate, "%m-%d-%Y").date()
        self.enddate = datetime.strptime(enddate, "%m-%d-%Y").date() + timedelta(1)

    def daterange(self):
        """Crates a generator over a list of dates"""
        # Borrowed from: http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
        for n in range(int((self.enddate - self.startdate).days)):
            yield self.startdate + timedelta(n)

    def create_links(self):
        """Creates list of CR links for each day in the date range"""
        return([self.url_prefix + d.strftime("%Y/%m/%d") + self.url_suffix for d in self.daterange()])

    def create_filenames(self):
        """Creates list of filenames for each day in the date range"""
        return([self.output_directory + "/" + self.house + str(d) + ".txt" for d in self.daterange()])

    def run(self):
        """Scrapes and saves Congressional Record for complete time period"""

        # Zip links and filenames and loop through
        for l, f in zip(self.create_links(), self.create_filenames):
            # Create scraper
            try:
                log.info("Retrieving content for " + l)
                s = CRScraper(l, f)
                s.run()
            # Catch exceptions
            except NoCRContentException:
                log.info("No content for " + l)
                continue

            s.save_file()

def main(args):
    CRWriter(args[0], args[1], args[2], args[3]).run()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Incorrect number of arguments. Program requires 4: house of congress (s/h), directory for saving transcripts, startdate (Y-m-d) and enddate (Y-m-d)")
        sys.exit()
    else:
        main(sys.argv[1:])
