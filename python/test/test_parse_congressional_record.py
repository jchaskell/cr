"""Tests CRParser class and helper functions"""

import os
import re
import sys
import unittest

from cr.parse_congressional_record import check_true, clean_file, CRParser, TITLE_INDICATOR

test_file = "test_page_filtered_content_total.txt"
resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

expected_titles = ["", 
                   "APPOINTMENT OF ACTING PRESIDENT PRO TEMPORE",
                   "EXECUTIVE SESSION: Tribute",
                   "EXECUTIVE SESSION: Liquid Nicotine"]

expected_speakers = [[""],
                     ["The PRESIDING OFFICER", "Mr. McCONNELL"],
                     ["Ms. COLLINS"],
                     ["Ms. COLLINS"]]

expected_speeches = [["Senate  The 2nd day of January being the day prescribed by House Joint Resolution 62 for the meeting of the 2d session of the 111th Congress, the Senate assembled in its Chamber at the Capitol at 12 and 10 seconds p.m., and was called to order by the Honorable Mark R. Warner, a Senator from the Commonwealth of Virginia"], 
                     ["The clerk will please read a communication to the Senate from the President pro tempore (Mr. Byrd).  The legislative clerk read the following letter:", "Zippity doo dah"],
                     ["In tribute to those who have died."],
                     ["Mr. President, bottles of liquid nicotine for e-cigarettes are bad for our kids."]]

class CRParserTest(unittest.TestCase):
    def setUp(self):
        test_file_path = os.path.join(resources_dir, test_file)
        self.test_parser = CRParser(test_file_path)

    def test_check_true(self):
        self.assertTrue(check_true("1"))
        self.assertTrue(check_true("True"))
        self.assertFalse(check_true("f"))

    def test_clean_file(self):
        test_input = "the quick brown fox"
        test_output_replace = clean_file(test_input, ["o", "x"], ["a", "z"])
        test_output_no_replace = clean_file(test_input, ["o", "x"])

        self.assertEqual(test_output_replace, "the quick brawn faz")
        self.assertEqual(test_output_no_replace, "the quick brwn f")

    def test_split_pages(self):
        # Speech, title, speaker should all be in the page listed in speech_to_page_mapping
        self.test_parser.split_pages()
        test_pages = self.test_parser.congressional_record_pages
        for i, page in enumerate(test_pages):
            # First speech is empty
            if page == '':
                continue
            for speech in expected_speeches[i - 1]:
                self.assertIn(speech, re.sub('\\\\n', '', page))
            
    def test_capture_title(self):
        self.test_parser.split_pages()
        test_pages = self.test_parser.congressional_record_pages
        no_title_expected = self.test_parser.capture_title(test_pages[1])
        title_expected = self.test_parser.capture_title(test_pages[2])

        self.assertEqual(no_title_expected, "")
        self.assertEqual(title_expected, expected_titles[1])

    def test_remove_title(self):
        self.test_parser.split_pages()
        test_pages = self.test_parser.congressional_record_pages
        page_with_no_title_before = test_pages[1]
        page_with_title_before = test_pages[2]
        page_with_no_title_after = self.test_parser.remove_title(page_with_no_title_before)
        page_with_title_after = self.test_parser.remove_title(page_with_title_before)

        self.assertEqual(page_with_no_title_before, page_with_no_title_after)
        self.assertFalse(re.search("[A-Z]{2,}", page_with_no_title_after))

    def test_add_speech_to_collection(self):
        self.test_parser.speeches["National Security"] = ["It is important."]
        expected_speeches = {
            "National Security": ["It is important.", "We spend too much."],
            "Environment": ["Nah, who cares."]
        }

        self.test_parser.add_speech_to_collection("National Security", "We spend too much.")
        self.test_parser.add_speech_to_collection("Environment", "Nah, who cares.")
        self.assertEqual(expected_speeches, self.test_parser.speeches)

    def test_add_titled_speeches_to_collect(self):
        self.test_parser.add_titled_speeches_to_collection()
        test_output = self.test_parser.speeches
        
        # Loop through and make sure speeches go with correct titles for the first two speeches (second 2 are parsed in next step)
        for i, speeches in enumerate(expected_speeches[:2]):
            test_page = test_output[expected_titles[i]]
            for x, y in zip(speeches, test_page):
                if y != '':
                    self.assertIn(x, re.sub('\\\\n', '', y))

    def parse_executive_session_speeches(self):
        self.test_parser.add_titled_speeches_collection()
        self.test_parser.parse_executive_session_speeches()
        test_output = self.test_parser.speeches

        # TODO: put some of this repetitive code in a function
        assertNotIn("EXECUTIVE SESSION", test_output.keys())
        for i, speeches in enumerate(expected_speeches[2:]):
            test_page = test_output(expected_titles[i])
            for x, y in zip(speeches, test_page):
                self.assertIn(x, re.sub('\\\\n', '', y))

    @unittest.skip("TODO")
    def test_filter_no_speakers(self):
        pass

    @unittest.skip("TODO")
    def test_match_for_speakers(self):
        pass

    @unittest.skip("TODO")
    def test_pull_out_record(self):
        pass

    @unittest.skip("TODO")
    def test_process_file(self):
        pass

    @unittest.skip("TODO")
    def test_write_file(self):
        pass

if __name__ == '__main__':
    unittest.main()
