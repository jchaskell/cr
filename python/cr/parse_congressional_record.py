"""Takes one file of Congressional Record scraping output and parses it into speeches"""

import os
import re
import sys

def check_true(x):
    return x.lower() in ("true", "yes", "t", "1")

def clean_file(file_text, strings_to_replace, replacements = None):
    """Cleans text by replacing strings_to_replace with replacements or with '' if replacements is not given
    
    : param file_text: string of text to clean
    : param strings_to_remove: list of strings to replace
    : param replacements: optional list of strings to replace; if not given, replace with '' 
    """

    if not replacements:
       replacements = [""] * len(strings_to_replace)
    
    for old, replace in zip(strings_to_replace, replacements):
        file_text.replace(old, replace)

    return(file_text)

class CRParser():
    def __init__(self, file_path):
    """Define a congressional record parser"""

    # Initialize 2 dictionaries for speeches and 'other' content
    # Nested dictionary of title -> speaker -> speeches
    self.speeches = {}
    self.other = {}

    with open(file_path) as f:
        self.text = f.read()

    def split_on_page_headers(self):
        """Splits pages and pulls out titles
        Updates self.speeches so that it is a dictionary of titles to text"""
        pass

    def pull_out_votes(self, vote_title = "Vote"):
        """Pulls out votes which will then be put in the 'other' file
        Updates self.other so that it includes votes with vote_title as the title
        Speaker is '' for votes; Takes votes out of speeches"""
        pass

    def filter_no_speakers(self):
        """Take out pages with no speakers and add them to 'other'
        Update both self.speeches and self.other"""
        pass

    def match_for_speakers(self):
        """Match for speakers and mark speakers; pull out speeches w/ no speakers
        Update self.speeches so they have both titles and speakers
        Update self.other to include text from pages with no speaker"""
        pass

    def pull_out_record(self):
        """Pull out text entered into record from speeches and add to other"""
        # Also need to clean up extra spaces and \n
        pass

    def process_file(self):
        """Does complete processing of 1 Congressional Record file"""
        pass

    def write_file(self, append, speeches_path, other_path = None):
        """Writes to files, either appending to existing files or writing to new ones"""
        pass

def main(file_path, append, output_file1, output_file2):
    parser = CRParser(file_path)
    parser.process_file()
    parser.write_file(append, output_file1, output_file2)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Too few arguments")
        sys.exit
    else:
        input_file = sys.argv[1]
        append = check_true(sys.argv[2])
        output_file1 = sys.argv[3]
        if len(sys.argv) >= 5:
            output_file2 = sys.argv[4]
        else:
            output_file2 = None
        main(input_file, append, output_file1, output_file2)
    

