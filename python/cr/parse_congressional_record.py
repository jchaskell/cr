"""Takes one file of Congressional Record scraping output and parses it into speeches"""
import argparse
from collections import OrderedDict
import csv
import os
import re
import sys


def check_true(x):
    return x.lower() in ("true", "yes", "t", "1")


def clean_file(file_text, strings_to_replace, replacements=None):
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


PAGE_BREAK_INDICATOR = "\[[\'\"](\\\\n)+\[[\'\"], <a href=[\'\"]/congressional-record/volume-\d+/(?:senate|house)-section/page/[SH][SH0-9\-]+[\'\"]>Pages? [HS][0-9\-HS]+</a>, u?[\'\"]\]\\\\nFrom the Congressional Record Online through the Government Publishing Office \[www\.gpo\.gov\]"
TITLE_INDICATOR = "^[\\\\n\s]*([A-Z0-9][A-Z0-9a-z \.,\-!\?:n]+)\n*"
SPEAKER_INDICATORS = [
    "(The PRESIDING OFFICER\.)",
    "(The ACTING PRESIDENT pro tempore)\.",
    "((Mr|Ms|Mrs)\.([A-Zace'\-]+)( [A-Z]+)?)\."
]
NON_SPEECH_TITLES = []


class CRParser():
    def __init__(self, file_path):
        """Define a congressional record parser"""

    # Nested dictionary of title -> speaker -> speeches
        self.speeches = OrderedDict()
        self.record = OrderedDict()

        with open(file_path) as f:
            self.congressional_record_text = f.read()

    def split_pages(self, page_break_regex=PAGE_BREAK_INDICATOR):
        self.congressional_record_pages = re.split(
            page_break_regex, self.congressional_record_text)

    def capture_title(self, page, title_regex=TITLE_INDICATOR):
        if not re.match(title_regex, page):
            title = ""
        else:
            title = re.match(title_regex, page).group(1)
        return(title)

    def remove_title(self, page):
        return(re.sub(TITLE_INDICATOR, "", page))

    def add_speech_to_collection(self, title, speech):
        if title in self.speeches.keys():
            self.speeches[title].append(speech)
        else:
            self.speeches[title] = [speech]

    def add_titled_speeches_to_collection(self):
        """Add speeches to collection, pulling out title if relevant"""
        # self.split_pages()

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

    # def parse_executive_session_speeches(self):
    #     # Make sure the title actually comes out this way
    #     if "EXECUTIVE SESSION" in self.speeches:
    #         for speech in self.speeches["EXECUTIVE_SESSION"]:
    #             titles = re.findall(TITLE_INDICATOR_EXEC_SESSION, speech)
    #             speeches = self.split_pages(TITLE_INDICATOR_EXEC_SESSION)
    #             for t, s in zip(titles, speeches):
    #                 self.add_speech_to_collection("EXECUTIVE SESSION: " + t, s)

    #         # Remove executive session from dictionary
    #         del self.speeches["EXECUTIVE_SESSION"]

    def print_speakers(self):
        # To start with, capture everything up to the second \. and print it out
        for title in self.speeches.keys():
            for speech in self.speeches[title]:

                match = ""
                m = re.

    def capture_speakers(self):
        # For a speech, use the speaker divider and get teh speakers
        # If a speech doesn't have a speaker, it seems like, if it starts with "Mr President"
        # or "Madam President", it still has a speaker but it's a continuation of the previous speech's speaker

        # To start with, capture everything up to the second \. and print it out
        for title in self.speeches.keys():
            for speech in self.speeches[title]:

                match = ""
                m = re.

    def match_speakers(self):
        """Match for speakers and mark speakers; pull out speeches w/ no speakers
        Update self.speeches so they have both titles and speakers
        Update self.other to include text from pages with no speaker"""
        pass

    def pull_out_record(self):
        """Pull out text entered into record from speeches and add to other"""
        # Also need to clean up extra spaces and \n
        pass

    def clean_speeches(self):
        # remove double \n\n to start speeches
        replacement = OrderedDict()
        for title in self.speeches.keys():
            speeches = []
            for speech in self.speeches[title]:
                s = re.sub('^[\n\s]+', '', speech)
                speeches.append(s)
            replacement[title] = speeches
        self.speeches = replacement

    # Run function for processing 1 CR file
    def process_file(self):
        """Does complete processing of 1 Congressional Record file"""
        self.split_pages()
        self.add_titled_speeches_to_collection()
        # parse_executive_session_speeches() - may still need another function for parsing titles,
        # but it looks ok right now
        self.clean_speeches()

    def write_file(self, append, speeches_path, other_path=None):
        """Writes to files, either appending to existing files or writing to new ones"""
        pass


def writer_helper(speeches, text_file_path="test.tsv"):
    labeled_text = []
    print(speeches.keys())
    for title in speeches.keys():
        for s in speeches[title]:
            no_newlines = re.sub('\\n', '', s)
            no_tabs = re.sub('\\t', '', no_newlines)
            labeled_text.append(f'{title}\t{no_tabs}')
    text = '\n'.join(labeled_text)

    with open(text_file_path, 'w') as f:
        f.write(text)


def main(file_path, append, output_file):
    parser = CRParser(file_path)
    parser.process_file()
    writer_helper(parser.speeches)


if __name__ == "__main__":
    # Input file; append; output file
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('append', type=bool)

    args = parser.parse_args()
    main(
        file_path=args.input_file,
        append=args.append,
        output_file=args.output_file
    )
