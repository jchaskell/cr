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
                   "APPOINTMENT OF ACTING PRESIDENT PRO TEMPORE",
                   "ADJOURNMENT UNTIL 11 A.M., TUESDAY, JANUARY 19, 2010"]

expected_speakers = ["",
                     "The PRESIDING OFFICER",
                     "Mr. McCONNELL",
                     "The ACTING PRESIDENT pro tempore"]

expected_speeches = ["Senate  The 2nd day of January being the day prescribed by House Joint Resolution 62 for the meeting of the 2d session of the 111th Congress, the Senate assembled in its Chamber at the Capitol at 12 and 10 seconds p.m., and was called to order by the Honorable Mark R. Warner, a Senator from the Commonwealth of Virginia", 
                     "The clerk will please read a communication to the Senate from the President pro tempore (Mr. Byrd).  The legislative clerk read the following letter:", 
                     "Zippity doo dah",
                     "Under the previous order, the Senate stands adjourned until 11 a.m. on Tuesday, January 19, 2010.  Thereupon, the Senate, at 12 and 43 seconds p.m., adjourned until Tuesday, January 19, 2010, at 11 a.m."]
speech_to_page_mapping = [1, 2, 2, 3]

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
        for index, x in enumerate(speech_to_page_mapping):
            self.assertIn(expected_speeches[index], re.sub('\\\\n', '', self.test_parser.congressional_record_pages[x]))

            self.assertIn(expected_titles[index], self.test_parser.congressional_record_pages[x])
            self.assertIn(expected_speakers[index], self.test_parser.congressional_record_pages[x])

    def test_capture_title(self):
        self.test_parser.split_pages()
        no_title_expected = self.test_parser.capture_title(self.test_parser.congressional_record_pages[1])
        title_expected = self.test_parser.capture_title(self.test_parser.congressional_record_pages[2])

        self.assertEqual(no_title_expected, "")
        self.assertEqual(title_expected, expected_titles[1])

    @unittest.skip("TODO: Write function")
    def test_split_on_page_headers(self):
        created_dictionary = test_parser.split_on_page_headers().speeches

        self.assertEqual(created_dictionary, expected_dictionary)

    @unittest.skip("TODO")
    def test_pull_out_votes(self):
        pass

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
