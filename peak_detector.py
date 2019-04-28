import os
import csv
import sys
from datetime import date, timedelta
import statistics

relevant_year = 2018


def get_volume(company_path):
    all_days = {}

    start_date = date(relevant_year, 1, 1)
    end_date = date(relevant_year + 1, 1, 1)
    difference = end_date - start_date

    for num_days in range(difference.days):
        new_day = start_date + timedelta(days=num_days)
        as_string = new_day.strftime('%Y-%m-%d')
        all_days[as_string] = 0

    with open(company_path, 'r') as f:
        reader = csv.reader(f)
        date_index = next(reader).index('date')
        for row in reader:
            # We know that date is in row 1
            row_date, _ = row[date_index].split(' ')
            row_year = row_date[0:4]

            if row_year != str(relevant_year):
                print(f'{row_year} tweet, discarding...')
                continue

            all_days[row_date] += 1

    return [all_days[day] for day in sorted(all_days.keys())]


def get_peaks(volumes, window_width, threshold):
    peaks = []

    for i in range(len(volumes)-2*window_width):
        day_index = i + window_width
        window = volumes[i:day_index+window_width+1]
        median = statistics.median(window)
        if volumes[day_index] > threshold * median:
            peaks.append(day_index)

    return peaks


def numbers_to_dates(first_day, peaks):
    year, month, day = first_day.split('-')
    beginning = date(int(year), int(month), int(day))
    dates = []

    for peak in peaks:
        offset = timedelta(days=peak)
        new_date = beginning + offset
        as_string = f'{new_date.year}-{new_date.month}-{new_date.day}'
        dates.append(as_string)

    return dates


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Requires a path to the tweet directory')
        sys.exit()

    tweets_directory = sys.argv[1]
    all_companies = [company for company in os.listdir(tweets_directory)
                     if os.path.isfile(os.path.join(tweets_directory,
                                                    company))]

    window_width = 5
    threshold = 2

    volumes = {}
    first_day = '2018-01-01'

    for company in all_companies:
        print(f'Data for {company}')
        company_path = os.path.join(tweets_directory, company)
        volumes[company] = get_volume(company_path)
        peaks = get_peaks(volumes[company], window_width, threshold)
        print(numbers_to_dates(first_day, peaks))
