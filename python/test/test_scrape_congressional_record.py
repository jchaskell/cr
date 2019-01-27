"""This module tests scrapeCR"""

import re
import unittest
from datetime import datetime

import requests
import requests_mock

from cr.scrape_congressional_record import CRWriter

startdate = "01-01-2010"
enddate = "01-02-2010"
tmp_directory = "temp"

class CRScraperTest(unittest.TestCase):
    # Need to create 2 test pages for the daily page - 1 with real content and 1 with none
    # Also need 2 test text pages 
    
    # TODO: write these tests
    expected_links

    def setUp(self):
        self.test_scraper = CRScraper()
        self.test_exception = CRScraper()

    def test_get_links(self):

        self.assertEqual( , self.expected_links)
        self.assertEqual( , [])

    def scrape_page(self):
        
    def save_file(self):
        # 


class CRWriterTest(unittest.TestCase):
    expected_dates = [datetime.strptime(startdate, "%m-%d-%Y").date(),
            datetime.strptime(enddate, "%m-%d-%Y").date()]
    expected_links = ["https://www.congress.gov/congressional-record/2010/01/01/senate-section",
            "https://www.congress.gov/congressional-record/2010/01/02/senate-section"]
    expected_filenames = ["temp/S2010-01-01.txt", "temp/S2010-01-02.txt"]

    def setUp(self):
        self.test_writer = CRWriter("s", tmp_directory, startdate, enddate)
        self.test_writer_house = CRWriter("h", tmp_directory, startdate, enddate)

    def test_daterange(self):
        self.assertEqual([d for d in self.test_writer.daterange()], self.expected_dates)

    def test_create_links(self):
        self.assertEqual(self.test_writer.create_links(), self.expected_links)
        self.assertEqual(self.test_writer_house.create_links(), [re.sub("senate", "house", link) for link in self.expected_links])

    def test_create_filenames(self):
        self.assertEqual(self.test_writer.create_filenames(), self.expected_filenames)
        self.assertEqual(self.test_writer_house.create_filenames(), [re.sub("S", "H", f) for f in self.expected_filenames])

    def test_run(self):
        # TODO: finish this test

if __name__ == '__main__':
    unittest.main()
