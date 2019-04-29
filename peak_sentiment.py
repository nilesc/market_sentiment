import csv

positive_emoji_path = 'positive.emoji'
negative_emoji_path = 'negative.emoji'

raw_positive_emoji_list = eval(open(positive_emoji_path, 'r').readline())
raw_negative_emoji_list = eval(open(negative_emoji_path, 'r').readline())

positive_emoji_list = [e.decode('utf-8') for e in raw_positive_emoji_list]
negative_emoji_list = [e.decode('utf-8') for e in raw_negative_emoji_list]


def get_sentiment_of_peaks(company_path, peaks):
    all_sentiments = {}
    with open(company_path, 'r') as f:
        reader = csv.reader(f)

        header_row = next(reader)
        date_index = header_row.index('date')
        emoji_index = header_row.index('emojis')


        for row in reader:
            tweet_date = row[date_index]
            emojis = row[emoji_index]

            tweet_sentiment = 0
            tweet_sentiment += sum([1 for emoji in positive_emoji_list
                                    if emoji in row[emoji_index]])

            tweet_sentiment -= sum([1 for emoji in negative_emoji_list
                                  if emoji in row[emoji_index]])

            if tweet_date not in all_sentiments:
                all_sentiments[tweet_date] = 0

            all_sentiments[tweet_date] += tweet_sentiment

    return all_sentiments
