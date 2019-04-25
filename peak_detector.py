import os
import sys

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Requires a path to the tweet directory')
        sys.exit()

    tweets_directory = sys.argv[1]
    for company in os.listdir(tweets_directory):
        print(company)
