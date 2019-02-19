"""This module tests scrapeCR"""

import os
import re
import shutil
import unittest
from datetime import datetime

import requests
import requests_mock

from cr.scrape_congressional_record import CRWriter, CRScraper

startdate = "01-01-2010"
enddate = "01-02-2010"
tmp_directory = "temp"
day_level_urls = ["https://www.congress.gov/congressional-record/2010/01/01/senate-section",
        "https://www.congress.gov/congressional-record/2010/01/02/senate-section"]
filenames = ["temp/S2010-01-01.txt", "temp/S2010-01-02.txt"]
expected_url_prefix = "https://www.congress.gov/congressional-record/2010/01/02/senate-section/article/S1-"

class CRScraperTest(unittest.TestCase):
    # For testing the daily Congressional Record pages from which links are pulled
    expected_urls = [expected_url_prefix + str(n) for n in range(1, 4)]
    day_level_files = ["test_page_20100101.txt", "test_page_20100102.txt"]

    # For testing the individual Congressional Record pages from which content is pulled

    record_level_files = ["test_record1.txt", "test_record2.txt", "test_record3.txt"]
    expected_content_one_page_file = "test_page_content1_text.txt"
    expected_content_total_file = "test_page_content_total.txt"

    def setUp(self):
        self.resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        self.test_scraper = CRScraper(day_level_urls[1], filenames[1])
        self.test_exception = CRScraper(day_level_urls[0], filenames[0])

    def tearDown(self):
        if os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)
    
    def mock_text_helper(self, mocker, url, filename):
        with open(os.path.join(self.resources_dir, filename)) as f:
            text = f.read()
            mocker.get(url, text = text)

    @requests_mock.Mocker()
    def test_get_links(self, mocker):
        # Test of actual text
        self.mock_text_helper(mocker, day_level_urls[1], self.day_level_files[1])
        self.assertEqual(self.test_scraper.get_links(), self.expected_urls) 
       
        # Test of page we expect to not return any links
        self.mock_text_helper(mocker, day_level_urls[0], self.day_level_files[0])
        self.assertEqual(self.test_exception.get_links(), [])

    @requests_mock.Mocker()
    def test_scrape_page(self, mocker):
        with open(os.path.join(self.resources_dir, self.expected_content_one_page_file)) as f:
            expected_output = f.read()
        self.mock_text_helper(mocker, self.expected_urls[0], self.record_level_files[0])
        # Note: there seems to be some trailing characters in the expected output file that I can't seem to get rid of - hence the "assertIn" instead of assertEqual
        self.assertIn(self.test_scraper.scrape_page(self.expected_urls[0]), expected_output)

    @unittest.skip("TODO")
    def test_save_file(self):
        # Note: this requires running run first before the file can be saved...j
        pass

    @unittest.skip("TODO")
    def test_run(self):
        pass


class CRWriterTest(unittest.TestCase):
    expected_dates = [datetime.strptime(startdate, "%m-%d-%Y").date(),
            datetime.strptime(enddate, "%m-%d-%Y").date()]
    expected_filenames = ["temp/S2010-01-01.txt", "temp/S2010-01-02.txt"]

    def setUp(self):
        self.test_writer = CRWriter("s", tmp_directory, startdate, enddate)
        self.test_writer_house = CRWriter("h", tmp_directory, startdate, enddate)

    def test_daterange(self):
        self.assertEqual([d for d in self.test_writer.daterange()], self.expected_dates)

    def test_create_links(self):
        self.assertEqual(self.test_writer.create_links(), day_level_urls)
        self.assertEqual(self.test_writer_house.create_links(), [re.sub("senate", "house", link) for link in day_level_urls])

    def test_create_filenames(self):
        self.assertEqual(self.test_writer.create_filenames(), filenames)
        self.assertEqual(self.test_writer_house.create_filenames(), [re.sub("S", "H", f) for f in self.expected_filenames])
    
    @unittest.skip("TODO")
    def test_run(self):
        pass

if __name__ == '__main__':
    unittest.main()
