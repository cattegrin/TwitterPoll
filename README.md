This script collects data from twitter and stores it in .xlsx format (Microsoft Excel Modern Format) This script is currently limited to collecting Tweets 'per minute'.

What I mean by this is that the Twitter API returns up to 100 results per query; Currently the script is set up so that each query collects tweets from a specific minute in time. I intend to revise this functionality to pull up to 100 results per 10-second period.

In it's current state, the script can pull up to 144,000 tweets from a single day with default settings. I advise changing the script parameters based on your data limit and needs.

Requirements: Twitter developer account and bearer access token

TO DO: Modify output to put time of each tweet in Spreadsheet Modify collection to grab tweets by second rather than minute