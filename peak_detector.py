import os
import csv
import sys
from datetime import date, timedelta, datetime
import statistics
from peak_sentiment import get_sentiment_of_peaks
import matplotlib.pyplot as plt
from scipy.stats import linregress

relevant_year = 2018

company_to_ticker = {'3M.csv': 'MMM',
        'Chevron.csv': 'CVX',
        'GoldmanSachs.csv': 'GS',
        'Merck.csv': 'MRK',
        'UTC.csv': 'UTX',
        'exxonmobil.csv': 'XOM',
        'AmericanExpress.csv': 'AXP',
        'Cisco.csv': 'CSCO',
        'HomeDepot.csv': 'HD',
        'Microsoft.csv': 'MSFT',
        'UnitedHealthGrp.csv': 'UNH',
        'intel.csv': 'INTC',
        'Apple.csv': 'AAPL',
        'CocaCola.csv': 'KO',
        'IBM.csv': 'IBM',
        'Nike.csv': 'NKE',
        'Visa.csv': 'V',
        'pfizer.csv': 'PFE',
        'Boeing.csv': 'BA',
        'Disney.csv': 'DIS',
        'JNJNews.csv': 'JNJ',
        'ProcterGamble.csv': 'PG',
        'Walgreens.csv': 'WBA',
        'verizon.csv': 'VZ',
        'Chase.csv': 'JPM',
        'DowDuPontCo.csv': 'DWDP',
        'McDonalds.csv': 'MCD',
        'Travelers.csv': 'TRV',
        'Walmart.csv': 'WMT'}


def get_volume(company_path):
    all_days = {}

    start_date = date(relevant_year, 1, 1)
    end_date = date(relevant_year + 1, 1, 1)
    difference = end_date - start_date

    for num_days in range(difference.days):
        new_day = start_date + timedelta(days=num_days)
        as_string = str(new_day)
        all_days[as_string] = 0

    with open(company_path, 'r') as f:
        reader = csv.reader(f)
        date_index = next(reader).index('date')
        for row in reader:
            # We know that date is in row 1
            row_date, _ = row[date_index].split(' ')
            row_year = row_date[0:4]

            # Ignore tweets from outside the range we're looking at
            if row_year != str(relevant_year):
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

    return numbers_to_dates(peaks)


def numbers_to_dates(peaks):
    beginning = date(relevant_year, 1, 1)
    dates = []

    for peak in peaks:
        offset = timedelta(days=peak)
        new_date = beginning + offset
        as_string = str(new_date)
        dates.append(as_string)

    return dates


def string_to_date(string):
    as_datetime = datetime.strptime(string, '%Y-%m-%d')
    return as_datetime.date()


def parse_finance_data(finance_path):
    all_data = {}

    with open(finance_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        ticker_index = header.index('ticker')
        close_index = header.index('Close')
        date_index = header.index('Date')

        for row in reader:
            ticker = row[ticker_index]
            close = row[close_index]
            date = row[date_index]

            if ticker not in all_data:
                all_data[ticker] = {}

            all_data[ticker][date] = close

    return all_data


def get_returns_for_dates(finance_data, company, dates):
    returns = {}
    company_data = finance_data[company]
    for peak_date in dates:
        as_date_object = string_to_date(peak_date)
        one_day_past = timedelta(days=-1)
        previous = as_date_object + one_day_past
        previous = str(previous)
        if peak_date not in company_data or previous not in company_data:
            continue
        day_return = float(company_data[peak_date]) / float(company_data[previous])

        returns[peak_date] = day_return

    return returns


def join_sentiments_and_returns(sentiments, returns):
    outputs = []
    for key in sentiments:
        if key not in returns:
            continue
        outputs.append((sentiments[key], returns[key]))
    return outputs


def linear_regression_p_value(points):
    x, y = zip(*points)
    _, _, _, p_value, _ = linregress(x, y)
    return p_value


def get_all_volume_peaks(tweets_directory, finance_path):
    finance_data = parse_finance_data(finance_path)

    all_companies = [company for company in os.listdir(tweets_directory)
                     if os.path.isfile(os.path.join(tweets_directory,
                                                    company))]

    window_width = 5
    threshold = 2

    volumes = {}
    first_day = '2018-01-01'

    scatter_points = {}

    for company in all_companies:
        ticker = company_to_ticker[company]
        company_path = os.path.join(tweets_directory, company)
        volumes[company] = get_volume(company_path)
        peaks = get_peaks(volumes[company], window_width, threshold)
        sentiments = get_sentiment_of_peaks(company_path, peaks)
        returns = get_returns_for_dates(finance_data, ticker, peaks)
        outputs = join_sentiments_and_returns(sentiments, returns)
        scatter_points[ticker] = outputs

    for company in scatter_points:
        print(linear_regression_p_value(scatter_points[company]))


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print('Requires a path to the tweet directory and finance file')
        sys.exit()

    tweets_directory = sys.argv[1]
    finance_path = sys.argv[2]
    get_all_volume_peaks(tweets_directory, finance_path)
