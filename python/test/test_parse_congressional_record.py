"""Tests CRParser class and helper functions"""

import os
import re
import sys
import unittest

from cr.parse_congressional_record import check_true, clean_file, CRParser

test_file = "test_page_filtered_content_total.txt"
resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
class CRParserTest(unittest.TestCase):
    def setUp(self):
        test_file_path = os.path.join(resources_dir, test_file)
        test_parser = CRParser(test_file_path)        
    
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

    @unittest.skip("TODO: Write function")
    def test_split_on_page_headers(self):
        created_dictionary = test_parser.split_on_page_headers().speeches

        expected_dictionary = {"": "\n\nSenate\n\n  The 2nd day of January being the day prescribed by House Joint \nResolution 62 for the meeting of the 2d session of the 111th Congress, \nthe Senate assembled in its Chamber at the Capitol at 12 and 10 seconds \np.m., and was called to order by the Honorable Mark R. Warner, a \nSenator from the Commonwealth of Virginia.\n\n                          ____________________\n\n\n']",
                               "APPOINTMENT OF ACTING PRESIDENT PRO TEMPORE": "The PRESIDING OFFICER. The clerk will please read a communication to \nthe Senate from the President pro tempore (Mr. Byrd).\n  The legislative clerk read the following letter:\n']",
                               "ADJOURNMENT UNTIL 11 A.M., TUESDAY, JANUARY 19, 2010": "The ACTING PRESIDENT pro tempore. Under the previous order, the \nSenate stands adjourned until 11 a.m. on Tuesday, January 19, 2010.\n  Thereupon, the Senate, at 12 and 43 seconds p.m., adjourned until \nTuesday, January 19, 2010, at 11 a.m.\n\n\n']"}

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
