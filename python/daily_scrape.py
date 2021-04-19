import argparse
from datetime import date, datetime, timedelta
import os
import sys

from cr.scrape_congressional_record import CRWriter

# Script for running Congressional Record Scraper Daily to update files


def get_start_date(directory):
    all_files = os.listdir(directory)

    # Get max date from file names
    file_dates = [x[1:] for x in all_files]
    file_dates.sort(reverse=True)
    latest_file = file_dates[0][:10]
    max_date = datetime(
        year=int(latest_file[:4]),
        month=int(latest_file[5:7]),
        day=int(latest_file[8:10])
    )

    start_date = max_date + timedelta(days=1)
    return start_date.strftime('%m-%d-%Y')


def main(directory):
    start_date = get_start_date(directory)
    today = date.today()
    todays_date = today.strftime('%m-%d-%Y')
    # Run House
    print(f'Running House for {start_date} to {todays_date}')
    CRWriter('h', directory, start_date, todays_date).run()
    # Run Senate
    print(f'Running Senate for {start_date} to {todays_date}')
    CRWriter('s', directory, start_date, todays_date).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str)
    args = parser.parse_args()
    main(args.directory)
