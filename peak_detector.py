import os
import csv
import sys


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


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Requires a path to the tweet directory')
        sys.exit()

    tweets_directory = sys.argv[1]
    all_companies = [company for company in os.listdir(tweets_directory)
                     if os.path.isdir(os.path.join(tweets_directory, company))]

    volumes = []

    for company in all_companies:
        company_dir = os.path.join(tweets_directory, company)
        volumes.append(get_volume(company_dir))

    print(f'Total number of companies: {len(volumes)}')
    print(f'Number with full representation: {sum([1 for volume in volumes if len(volume) == 364])}')
