# This script was used to pull historical posts from various Subreddits (communities) on social media platform Reddit using Pushshift Reddit API

# Import required libraries
import requests
import pandas as pd
import time
from datetime import timedelta
from requests.adapters import HTTPAdapter
import json
from sqlalchemy import create_engine, exc


# Create an SQL engine to store the fetched posts content from a subreddit to reddit.db database on local disk. The address on local disk can be changed as per convenience
engine = create_engine(
    f'sqlite:///C:/Users/Akshay/Desktop/ClimateChange/Database/reddit.db')

# Function to create a table in local reddit.db database to store the fetched data


def create_table(name):
    """
    The following variables are stored in the SQL database for each post fetched from a given subreddit using Pushshift API;
    i :			unique id assigned to each Reddit post fetched from Pushshift API
    utc :		timestamp (Unix epoch time)
    title :		headline of the Reddit post (text)
    post :		main body of the post (if available, text)
    author : 	reddit id of the person who created the post (text)
    score :		simply the number of upvotes minus the number of downvotes (integer)
    upratio :	proportion of upvotes (float), =(upvotes/(upvotes+downvotes)), a recent metric; only available for c.10% of the data
    numcom :	total no. of comments on the post (integer)
    awards :	given by other users, higher the number more appreciation the post gets (integer)
    crossp :	total no. of crossposts (shares) by other Reddit users, similar to ReTweets on Twitter (integer)
    link :		actual link to the reddit post
    subreddit : subcommunity in which the post appeared
    """
    sql = f"CREATE TABLE IF NOT EXISTS {name} (i integer, utc datetime, title text, post text, author text, score integer, upratio float, numcom integer, awards integer, crossp integer, link text, subreddit text, PRIMARY KEY (i))"
    engine.execute(sql)


# Create a new table "A" (titled randomly) using above function with specified sql query in place.
# Another copy of this script was used simultaneously to speed up the data collection process
# A new table "B" was created in reddit.db database to save the data simulataneously from the second script
create_table("A")


# Create a requests session and mount HTTPAdapter
s = requests.Session()
s.mount('https://', HTTPAdapter(max_retries=2))
#s.mount('http://', HTTPAdapter(max_retries=2))

# Header to be used as a parameter in get() method of requests module
headers = {
    'Referer': 'https://www.google.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}


# Provide the end time for historical data collection. Provided below June 30, 2021 (input in Unix epoch time format). The value can be changed as per convenience
before = '1625036292'

# Empty dictionary to collect the fetched data for each Reddit post initialised with a counter for number of posts fetched
articles = {}
count = 0

# Just a counter to update the number of times the data was pushed to SQL database and timer to measure the time at beginning
times_saved = 0
start_t = time.monotonic()

# Load the list of all the climate related subreddits (communities) on Reddit from which users posts data is needed to be extracted
# The list is created and managed manually in a text file
with open('ClimateSubredditsList.txt', 'r') as f:
    communities = [line.strip() for line in f]


# Loop through every subreddit (community) in the list, one at a time to fetch all of the historical posts made by users in the respective subreddits
for subred in communities:

    print(f"Scraping {subred} now...\n")

    # Provide the start time for historical data collection. Provided below Jan 01, 2006 (input in Unix epoch time format). The value can be changed as per convenience
    after = '1136139768'

    while True:

        # Select Pushshift API endpoint as url to fetch data. Provide "subred", "after" and "before" as variables to loop through each subreddit and over time
        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subred}&sort=asc&sort_type=created_utc&after={after}&before={before}&size=1000"
        attempt = 0

        while True:
            response = None
            try:
                response = s.get(url, headers=headers, timeout=20)
                data = response.json()
                break
            except Exception as err:
                attempt += 1
                print(
                    f'Caught {err}... Sleeping for 10 sec and then retrying...')
                time.sleep(10)
                if attempt <= 20:
                    continue
                else:
                    break

        # After a single page of data is fetched from API, loop through all the posts in it one at a time and select only the variables that are required
        for article in data['data']:

            try:
                created_utc = article['created_utc']
            except Exception as e:
                created_utc = 'NaN'

            try:
                title = article['title']
            except Exception as e:
                title = 'NaN'

            try:
                selftext = article['selftext']
            except Exception as e:
                selftext = 'NaN'

            try:
                author = article['author']
            except Exception as e:
                author = 'NaN'

            try:
                score = article['score']
            except Exception as e:
                score = 'NaN'

            try:
                upvote_ratio = article['upvote_ratio']
            except Exception as e:
                upvote_ratio = 'NaN'

            try:
                num_comments = article['num_comments']
            except Exception as e:
                num_comments = 'NaN'

            try:
                total_awards_received = article['total_awards_received']
            except Exception as e:
                total_awards_received = 'NaN'

            try:
                num_crossposts = article['num_crossposts']
            except Exception as e:
                num_crossposts = 'NaN'

            try:
                full_link = article['full_link']
            except Exception as e:
                full_link = 'NaN'

            try:
                subreddit = article['subreddit']
            except Exception as e:
                subreddit = 'NaN'

            # Increase the post count by 1 for each post retrieved
            count += 1

            # Append the fetched data from each post to the empty "articles" dictionary declared at the beginning of the script, with count no. as key for each post
            articles[count] = [count, created_utc, title, selftext, author, score,
                               upvote_ratio, num_comments, total_awards_received,
                               num_crossposts, full_link, subreddit]

            # Not in use countermeasure; just to give enough sleep time in between while making large number of server requests
            # if count in [20000,30000,40000]:
            #   time.sleep(30)

            # A counter, that prints number of articles fetched in a multiple of 500
            if count % 500 == 0:
                now_t = time.monotonic()
                print('Posts: ', count, " | Time taken: ",
                      timedelta(seconds=now_t - start_t))

            # Save the fetched data to reddit.db database every time the pulled posts count reaches 50,000
            if count % 50000 == 0:
                # Increase the no. of times data is pushed to SQL database by 1
                times_saved += 1
                print('Total Count', count)
                end_time = time.monotonic()
                print(
                    f'Times saved - {times_saved} | Running since: {timedelta(seconds=end_time - start_t)} | Subred - {subreddit}')
                # print('\n\n')

                # Create a dataframe with data from articles dictionary and provide respective column titles
                df = pd.DataFrame.from_dict(articles, orient='index', columns=['i', 'utc', 'title', 'post', 'author',
                                                                               'score', 'upratio', 'numcom', 'awards',
                                                                               'crossp', 'link', 'subreddit'])

                df['title'] = df['title'].map(
                    lambda x: x.encode('unicode-escape').decode('utf-8'))
                df['link'] = df['link'].map(
                    lambda x: x.encode('unicode-escape').decode('utf-8'))
                df['post'] = df['post'].map(
                    lambda x: x.encode('unicode-escape').decode('utf-8'))
                df['author'] = df['author'].map(
                    lambda x: x.encode('unicode-escape').decode('utf-8'))
                df['subreddit'] = df['subreddit'].map(
                    lambda x: x.encode('unicode-escape').decode('utf-8'))

                print('Saving to SQLite database...\n\n')

                # Append the dataframe to SQL table
                df.to_sql("A", engine, if_exists='append', index=False)

                # Reset the articles dictionary to empty to store new posts to be fetched from Reddit
                articles = {}
                time.sleep(5)

        # Check if more posts exist in a given subreddit or if end date is reached
        new_after = f"{created_utc}"
        if int(new_after) < int(before) and new_after != after:
            after = new_after
            print("More posts available...\n")
            continue
        else:
            print("No more posts available...\n")
            break


# After looping through all the subreddits in the list provided earlier, the final unsaved articles dictionary of posts with count < 50000 is pushed to SQL database using this part of the script
# Increase the no. of times data is pushed to SQL database by 1
times_saved += 1
print('Total Count', count)
end_time = time.monotonic()
print(
    f'Times saved - {times_saved} | Running since: {timedelta(seconds=end_time - start_t)} | Subred - {subreddit}')

# Same as earlier, create a dataframe from articles dictionary and append it to SQL database
df = pd.DataFrame.from_dict(articles, orient='index', columns=['i', 'utc', 'title', 'post', 'author',
                                                               'score', 'upratio', 'numcom', 'awards',
                                                               'crossp', 'link', 'subreddit'])

df['title'] = df['title'].map(
    lambda x: x.encode('unicode-escape').decode('utf-8'))
df['link'] = df['link'].map(
    lambda x: x.encode('unicode-escape').decode('utf-8'))
df['post'] = df['post'].map(
    lambda x: x.encode('unicode-escape').decode('utf-8'))
df['author'] = df['author'].map(
    lambda x: x.encode('unicode-escape').decode('utf-8'))
df['subreddit'] = df['subreddit'].map(
    lambda x: x.encode('unicode-escape').decode('utf-8'))
print('Saving to SQLite database...\n\n')

df.to_sql("A", engine, if_exists='append', index=False)

print("Finished fetching data from all of the communitites!")
