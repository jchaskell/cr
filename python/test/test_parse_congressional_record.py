"""Tests CRParser class and helper functions"""

import os
import re
import sys
import unittest

from cr.parse_congressional_record import check_true, clean_file, CRParser

class CRParserTest(unittest.TestCase):
    def test_check_true(self):
        self.assertTrue(check_true("1"))
        self.assertTrue(check_true("True"))
        self.assertFalse(check_true("f"))

    @unittest.skip("TODO")
    def test_clean_file(self):
        pass

    @unittest.skip("TODO")
    def test_split_on_page_headers(self):
        pass

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
