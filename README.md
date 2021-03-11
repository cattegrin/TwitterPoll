# TwitterPoll
Collects tweets from the Twitter API using a search query. Result is spreadsheet with up to 100 tweets per minute worth of data

REQUIREMENTS:
  Twitter Developer Account & Bearer Token

TODO:
  output tweet creation date to spreadsheet
  improve memory efficiency 
  make script easier to configure
  allow script to query specific seconds rather than minutes. 
  
  
NOTES:
  By default, the script polls for a maximum of 100 tweets per query. Each query searches a specific minute in time. 
  This means that each output sheet will contain up to 144,000 tweets (24*60*100)
