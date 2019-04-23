import sys
import csv
import time
import pandas
from yahoo_quote_download.yahoo_quote_download import yqd

def get_data(tickers):
    start = '20180101'
    end = '20190101'

    responses = []
    written_header = False

    for t in tickers:
        # Remove the trailing newline
        cleaned = t[:-1]
        response = yqd.load_yahoo_quote(cleaned, start, end, format_output='dataframe')
        ticker_col = [cleaned] * response.shape[0]
        response['ticker'] = ticker_col
        responses.append(response)

        # Insert delay to be nice
        time.sleep(0.1)

    return pandas.concat(responses)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Must provide a file to read tickers from")
        sys.exit()

    ticker_file = open(sys.argv[1], 'r')
    data = get_data(ticker_file)
    data.to_csv(path_or_buf='output.csv', index=False)
