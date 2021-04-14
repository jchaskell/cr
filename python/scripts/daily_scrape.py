# Script for running Congressional Record Scraper Daily to update files
from datetime import datetime
import os, sys

# List files

def main(directory):
    date_range = get_date_range(directory)
    # Run House
    print(f'Running House for {date_range.start} to {date_range.end}')
    # Run Senate
    print(f'Running Senate for {date_range.start} to {date_range.end}')


if __name__ == "__main__":
    # Use argparse to parse arguments    
    