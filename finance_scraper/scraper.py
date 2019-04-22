import sys
from yahoo_quote_download.yahoo_quote_download import yqd

def get_data(tickers):
    start = '20180101'
    end = '20190101'

    responses = []

    for t in tickers:
        cleaned = t[:-1]
        responses.append(yqd.load_yahoo_quote(cleaned, start, end))

    print(len(responses))
    return responses

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Must provide a file to read tickers from")
        sys.exit()

    ticker_file = open(sys.argv[1], 'r')
    print(get_data(ticker_file))
