"i""Takes one file of Congressional Record scraping output and parses it into speeches"""

import csv
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
        file_text = file_text.replace(old, replace)
    return(file_text)

PAGE_BREAK_INDICATOR = "\[[\'\"]\\\\n\[[\'\"], <a href=[\'\"]/congressional-record/volume-\d+/(?:senate|house)-section/page/[SH]\d+[\'\"]>Page [HS][0-9-]+</a>, u?[\'\"]\]\\\\nFrom the Congressional Record Online through the Government Publishing Office \[www\.gpo\.gov\]"

TITLE_INDICATOR = "^[\\\\n\s]*([A-Z0-9 \.,\-!\?]{2,})[\\n\s]*"
TITLE_INDICATOR_EXEC_SESSION = "^\s+([A-Za-z\s\.\,:\-]+)[\\\\n]{2}"

class CRParser():
    def __init__(self, file_path):
        """Define a congressional record parser"""

    # Nested dictionary of title -> speaker -> speeches
        self.speeches = {}
        self.other = {}

        with open(file_path) as f:
            self.congressional_record_text = f.read()

    def split_pages(self, page_break_regex = PAGE_BREAK_INDICATOR):
        self.congressional_record_pages = re.split(page_break_regex, self.congressional_record_text)

    def capture_title(self, page, title_regex = TITLE_INDICATOR):
        if not re.match(title_regex, page):
            title = ""
        else:
            title = re.match(title_regex, page).group(1)
        return(title)

    def remove_title(self, page):
        return(re.sub(TITLE_INDICATOR, "", page))

    def add_speech_to_collection(self, title, speech):
        if self.speeches and title in self.speeches:
            self.speeches[title].append(speech)
        else:
            self.speeches[title] = [speech]

    def add_titled_speeches_to_collection(self):
        """Add speeches to collection, pulling out title if relevant"""
        self.split_pages()
        
        for page in self.congressional_record_pages:
            title = self.capture_title(page)
            # Don't bother with empty text
            if not re.match("^\s+$", page):
                if title:
                    page_text = self.remove_title(page)
                    self.add_speech_to_collection(title, page_text)
                else:
                    self.add_speech_to_collection("", page) 

    # Let's not pull out votes. Let's do that in a deeper parsing script.

    # Function for cleaning up text either here or after pulling out speeches
    
    def parse_executive_session_speeches(self):
        # Make sure the title actually comes out this way
        if "EXECUTIVE SESSION" in self.speeches:
            for speech in self.speeches["EXECUTIVE_SESSION"]:
                titles = re.findall(TITLE_INDICATOR_EXEC_SESSION, speech)
                speeches = self.split_pages(TITLE_INDICATOR_EXEC_SESSION)
                for t, s in zip(titles, speeches):
                    self.add_speech_to_collection("EXECUTIVE SESSION: " + t, s)
                    
            # Remove executive session from dictionary
            del self.speeches["EXECUTIVE_SESSION"]
            
   # This needs to come before executive session 
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

    # Run function for processing 1 CR file
    def process_file(self):
        """Does complete processing of 1 Congressional Record file"""
        split_pages()
        add_titles_speeches_to_collection()
        parse_executive_session_speeches()

    def write_file(self, append, speeches_path, other_path = None):
        """Writes to files, either appending to existing files or writing to new ones"""
        pass

def writer_helper(speeches, text_file_path = "test.csv"):
    with open(text_file_path, 'w') as f:
        writer = csv.DictWriter(f, ["title", "speech"])
        writer.writeheader()
        for speech in speeches:
            writer.writerow(speech)

def main(file_path, append, output_file1, output_file2):
    parser = CRParser(file_path)
    parser.process_file()
    #parser.write_file(append, output_file1, output_file2)
    writer_helper(parser.speeches)    

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
    

