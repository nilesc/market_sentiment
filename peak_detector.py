import os
import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Requires a path to the tweet directory')
        sys.exit()

    tweets_directory = sys.argv[1]
    all_companies = [company for company in os.listdir(tweets_directory)
                     if os.path.isdir(os.path.join(tweets_directory, company))]
    for company in all_companies:
        print(f'Analyzing: {company}')
        company_dir = os.path.join(tweets_directory, company)
        all_days = sorted(os.listdir(company_dir))
        tweet_volume = []
        for day in all_days:
            day_path = os.path.join(company_dir, day)
            with open(day_path, 'r') as f:
                reader = csv.reader(f)
                day_volume = sum([1 for row in reader])
                tweet_volume.append(day_volume)
        print(tweet_volume)
        print()
