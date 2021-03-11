import requests
import datetime
import time
import xlsxwriter


class Tweet:                        # Class to hold data related to tweets
    def __init__(self, text=None, date=None):
        self.text = text
        self.d = date


class Day:                          # Class to track tweets on a certain date
    def __init__(self, date):
        self.d = date
        self.tweets = []

    def add_tweet(self, t):
        self.tweets.append(t)


bear_file = open('bear.txt','r')
TOKEN = bear_file.read()
bear_file.close()


def search_twitter(query, tweet_fields, start, end, depth, bearer_token=TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}&{}".format(
        query, tweet_fields, start, end, depth
    )

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_minute(offset, s, e):
    query = "doge%20(%23doge)%20-is:verified"
    fields = "tweet.fields=text,created_at"
    depth = "max_results=100"

    start_date = (s - datetime.timedelta(hours=offset)).replace(microsecond=0).isoformat()
    end_date = (e - datetime.timedelta(hours=offset)).replace(microsecond=0).isoformat()

    start = "start_time=" + str(start_date) + "Z"
    end = "end_time=" + str(end_date) + "Z"

    resp = search_twitter(query, fields, start, end, depth)

    text = []

    for r in resp['data']:
        encoded = str(r['text']).encode("ascii", "ignore")
        text.append(encoded.decode())

    return text


def get_hour(offset, s, e):
    start_date = (s - datetime.timedelta(hours=offset)).replace(microsecond=0)
    end_date = (e - datetime.timedelta(hours=offset)).replace(microsecond=0)

    text = []
    x = 0
    while x < 60:
        text.append(get_minute(x, start_date, end_date))
        x += 1
        time.sleep(5)

    return text


def get_day(offset):
    start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=offset, minutes=1))
    end_date = (datetime.datetime.utcnow() - datetime.timedelta(days=offset-1, minutes=1))

    x=0
    text = []
    while x < 24:
        text.append(get_hour(x, start_date, end_date))
        x += 1

    return text

x=1
while x < 4:
    workbook = xlsxwriter.Workbook(str((datetime.datetime.utcnow() - datetime.timedelta(days=x)).replace(microsecond=0).isoformat())[0:10] + ".xlsx")
    sheet = workbook.add_worksheet()
    # output_file = open(str((datetime.datetime.utcnow() - datetime.timedelta(days=x)).replace(microsecond=0).isoformat())[0:10]+".txt", 'w+')
    data = get_day(x)

    row = 0
    col = 0
    for hour in data:
        for min in hour:
            for t in min:
                sheet.write(row, col, t)
                row += 1
                # output_file.write(t+'\n')
    # output_file.close()
    x += 1
    workbook.close()




