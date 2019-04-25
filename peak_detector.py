import os
import csv
import sys
import statistics


def get_volume(company_dir):
    all_days = sorted(os.listdir(company_dir))
    tweet_volume = []
    for day in all_days:
        day_path = os.path.join(company_dir, day)
        with open(day_path, 'r') as f:
            reader = csv.reader(f)
            day_volume = sum([1 for row in reader])
            tweet_volume.append(day_volume)
    return tweet_volume


def get_peaks(volumes, window_width, threshold):
    peaks = []

    for i in range(len(volumes)-2*window_width):
        day_index = i + window_width
        window = volumes[i:day_index+window_width+1]
        median = statistics.median(window)
        if volumes[day_index] > threshold * median:
            peaks.append(day_index)

    return peaks


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Requires a path to the tweet directory')
        sys.exit()

    tweets_directory = sys.argv[1]
    all_companies = [company for company in os.listdir(tweets_directory)
                     if os.path.isdir(os.path.join(tweets_directory, company))]

    window_width = 5
    threshold = 2

    volumes = {}

    for company in all_companies:
        print(f'Data for {company}')
        company_dir = os.path.join(tweets_directory, company)
        volumes[company] = get_volume(company_dir)
        peaks = get_peaks(volumes[company], window_width, threshold)
        print(peaks)

    print(f'Total number of companies: {len(volumes)}')
    print(f'Number with full representation: {sum([1 for volume in volumes if len(volumes[volume]) == 364])}')
