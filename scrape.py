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


bear_file = open('bear.txt','r')                # Gets Bearer token from file
TOKEN = bear_file.read()
bear_file.close()


def search_twitter(query, tweet_fields, start, end, depth, bearer_token=TOKEN):
    '''
    :param query: The query to search
    :param tweet_fields: Data to collect for each result
    :param start: Start time of search
    :param end: End time of search
    :param depth: Depth of search (max 100)
    :param bearer_token: Token to access API
    :return: json data of response
    '''
    headers = {"Authorization": "Bearer {}".format(bearer_token)}                   # Sets request header

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}&{}".format( # Generates API request
        query, tweet_fields, start, end, depth
    )

    response = requests.request("GET", url, headers=headers)                    # Makes API request

    if response.status_code != 200:                                             # Checks if we got an error
        raise Exception(response.status_code, response.text)
    return response.json()                                                      # Returns API response


def get_minute(offset, s, e):
    '''
    :param offset: Number of minutes to offset by
    :param s: Search start time
    :param e: Search end time
    :return: Array of text representing all tweets gathered for a specific minute
    '''
    query = "doge%20(%23doge)%20-is:verified"               # Query to search
    fields = "tweet.fields=text,created_at"                 # Fields of tweet to return
    depth = "max_results=100"                               # Max results per query

    start_date = (s - datetime.timedelta(hours=offset)).replace(microsecond=0).isoformat()  # Sets start time
    end_date = (e - datetime.timedelta(hours=offset)).replace(microsecond=0).isoformat()    # Sets end time

    start = "start_time=" + str(start_date) + "Z"                                           # Configures param
    end = "end_time=" + str(end_date) + "Z"

    resp = search_twitter(query, fields, start, end, depth)                                 # Sends search info to func

    text = []

    for r in resp['data']:                                                                  # For all tweets
        encoded = str(r['text']).encode("ascii", "ignore")                                  # Remove non ascii chars
        text.append(encoded.decode())                                                       # Add to data set

    return text


def get_hour(offset, s, e):
    '''
    :param offset: Number of hours to offset by
    :param s: Search start hour
    :param e: Search end hour
    :return: Array of minutes, where each minute is an arrya of up to 100 tweets from that minute
    '''
    start_date = (s - datetime.timedelta(hours=offset)).replace(microsecond=0)  # Sets start time
    end_date = (e - datetime.timedelta(hours=offset)).replace(microsecond=0)    # Sets end time

    text = []
    x = 0
    while x < 60:                                               # Loops through all minutes of hour
        text.append(get_minute(x, start_date, end_date))        # Appends data to array
        x += 1
        time.sleep(5)                                           # Sleeps to not stress out the API

    return text                                                 # Returns hour worth of data


def get_day(offset):
    '''
    :param offset: Number of days to offset by
    :return: Array of hours, where each hour is an array of minutes,
                where each minute is up to 100 tweets from that minute
    '''
    start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=offset, minutes=1))  # Increments start time
    end_date = (datetime.datetime.utcnow() - datetime.timedelta(days=offset, minutes=2))  # Increments end time

    x=0
    text = []
    while x < 24:                                       # Loops through all hours of day
        text.append(get_hour(x, start_date, end_date))  # Searches for an hour of data and appends to day array.
        x += 1                                          # Increments hour index

    return text                                         # Returns data for day


x = 1                                 # Sets counter var
while x < 4:                        # Number of recent days to collect data for
    workbook = xlsxwriter.Workbook(str((datetime.datetime.utcnow()
                                        - datetime.timedelta(days=x)).replace(microsecond=0)
                                       .isoformat())[0:10] + ".xlsx")                   # Opens excel workbook for day
    sheet = workbook.add_worksheet()                                                    # Adds base sheet to workbook
    # output_file = open(str((datetime.datetime.utcnow()
    # - datetime.timedelta(days=x)).replace(microsecond=0)
    # .isoformat())[0:10]+".txt", 'w+')
    data = get_day(x)                                                                   # Gets a day's worth of data

    row = 0
    col = 0
    for hour in data:                                                               # Inserts data in sheet
        for min in hour:
            for t in min:
                sheet.write(row, col, t)
                row += 1
                # output_file.write(t+'\n')
    # output_file.close()
    x += 1
    workbook.close()                                        # Closes workbook




