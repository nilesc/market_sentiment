from yahoo_quote_download.yahoo_quote_download import yqd

ticker = ['QCOM', 'C', '^DJI']

start = '20190101'
end = '20190127'
for t in ticker:
    print(yqd.load_yahoo_quote(t, start, end))
