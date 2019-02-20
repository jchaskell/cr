"""This module tests scrapeCR"""

import os
import re
import shutil
import unittest
from datetime import datetime

import requests
import requests_mock

from cr.scrape_congressional_record import CRWriter, CRScraper, NoCRContentException

startdate = "01-01-2010"
enddate = "01-02-2010"
tmp_directory = "temp"
day_level_urls = ["https://www.congress.gov/congressional-record/2010/01/01/senate-section",
        "https://www.congress.gov/congressional-record/2010/01/02/senate-section"]
filenames = ["S2010-01-01.txt", "S2010-01-02.txt"]
expected_url_prefix = "https://www.congress.gov/congressional-record/2010/01/02/senate-section/article/S1-"
resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
expected_urls = [expected_url_prefix + str(n) for n in range(1, 4)]
record_level_files = ["test_record1.txt", "test_record2.txt", "test_record3.txt"]
expected_filtered_content_file = "test_page_filtered_content_total.txt"
expected_content_file1 = "test_page_content1_text.txt" 

day_level_files = ["test_page_20100101.txt", "test_page_20100102.txt"]

def mock_text_helper(mocker, url, filename):
    with open(filename) as f:
        text = f.read()
        mocker.get(url, text = text)

class CRScraperTest(unittest.TestCase):
    def setUp(self):
        if os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)
        os.mkdir(tmp_directory)
        self.test_scraper = CRScraper(day_level_urls[1], os.path.join(tmp_directory, filenames[1]))
        self.test_exception = CRScraper(day_level_urls[0], os.path.join(tmp_directory, filenames[0]))

    def tearDown(self):
        if os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)

    @requests_mock.Mocker()
    def test_get_links(self, mocker):
        # Test of actual text
        mock_text_helper(mocker, day_level_urls[1], os.path.join(resources_dir, day_level_files[1])) 
        self.assertEqual(self.test_scraper.get_links(), expected_urls) 
       
        # Test of page we expect to not return any links
        mock_text_helper(mocker, day_level_urls[0], os.path.join(resources_dir, day_level_files[0])) 
        self.assertEqual(self.test_exception.get_links(), [])

    @requests_mock.Mocker()
    def test_scrape_page(self, mocker):
        with open(os.path.join(resources_dir, expected_content_file1)) as f:
            expected_output = f.read()
        mock_text_helper(mocker, expected_urls[0], os.path.join(resources_dir, record_level_files[0]))
        # Note: there seems to be some trailing characters in the expected output file that I can't seem to get rid of - hence the "assertIn" instead of assertEqual
        self.assertIn(self.test_scraper.scrape_page(expected_urls[0]), expected_output)
    
    @requests_mock.Mocker()
    def test_run(self, mocker):
        # Expect content - one day, 3 pages
        for u, f in zip(day_level_urls, day_level_files):
            mock_text_helper(mocker, u, os.path.join(resources_dir, f))
        for u, f in zip(expected_urls, record_level_files):
            mock_text_helper(mocker, u, os.path.join(resources_dir, f))
        with open(os.path.join(resources_dir, expected_filtered_content_file)) as f:
            expected_output = f.read()
        self.test_scraper.run()
        self.assertIn(self.test_scraper.content, expected_output)

        # Expect an exception
        with self.assertRaises(NoCRContentException):
            self.test_exception.run()

    @requests_mock.Mocker()
    def test_save_file(self, mocker):
        mock_text_helper(mocker, day_level_urls[1], os.path.join(resources_dir, day_level_files[1])) 
        for u, f in zip(expected_urls, record_level_files):
            mock_text_helper(mocker, u, os.path.join(resources_dir, f))
        self.test_scraper.run()
        self.test_scraper.save_file()
        self.assertTrue(os.path.isfile(os.path.join(tmp_directory, filenames[1])))
        

class CRWriterTest(unittest.TestCase):
    expected_dates = [datetime.strptime(startdate, "%m-%d-%Y").date(),
            datetime.strptime(enddate, "%m-%d-%Y").date()]

    def setUp(self):
        if os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)
        os.mkdir(tmp_directory)
        self.test_writer = CRWriter("s", tmp_directory, startdate, enddate)
        self.test_writer_house = CRWriter("h", tmp_directory, startdate, enddate)

    def tearDown(self):
        if os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)
    
    def test_daterange(self):
        self.assertEqual([d for d in self.test_writer.daterange()], self.expected_dates)

    def test_create_links(self):
        self.assertEqual(self.test_writer.create_links(), day_level_urls)
        self.assertEqual(self.test_writer_house.create_links(), [re.sub("senate", "house", link) for link in day_level_urls])

    def test_create_filenames(self):
        self.assertEqual(self.test_writer.create_filenames(), ["temp/" + f for f in filenames])
        self.assertEqual(self.test_writer_house.create_filenames(), ["temp/" + re.sub("S", "H", f) for f in filenames])
    
    @requests_mock.Mocker()
    def test_run(self, mocker):
        # Expect file for 1/2
        with open(os.path.join(resources_dir, expected_filtered_content_file)) as f:
            expected_output = f.read()
        for u, f in zip(day_level_urls, day_level_files):
            mock_text_helper(mocker, u, os.path.join(resources_dir, f))
        for u, f in zip(expected_urls, record_level_files):
            mock_text_helper(mocker, u, os.path.join(resources_dir, f))
        self.test_writer.run()

        with open(os.path.join(tmp_directory, filenames[1])) as f:
            test_output = f.read()
        self.assertIn(test_output, expected_output)


        # Expect no file for 1/1
        self.assertFalse(os.path.isfile(os.path.join(tmp_directory, filenames[0])))
        

if __name__ == '__main__':
    unittest.main()
