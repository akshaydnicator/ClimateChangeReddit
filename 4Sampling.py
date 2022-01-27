# This script was used to obtain Sample 1 and 2 time-series from c.1m selected Reddit posts

# Import required libraries
import numpy as np
import pandas as pd
from datetime import timedelta

# Load the cleaned preprocessed data from "PreProcessedData.csv" file saved in the previous step
df = pd.read_csv("PreProcessedData.csv")
df["date"] = pd.to_datetime(df["date"])

# Exclude the posts that are from "EcoInternet" subreddit (outlier - active only in 2017-18); single user rersponsible for c.35% of the total posts collected
df = df[df["subreddit"] != "EcoInternet"]
df.drop_duplicates(subset=["clean_text"], inplace=True)
print(len(df))


# Initialize start and end dates. First post in the database has published date in Jan 2008. So a start was picked before that month in Dec 2007
# Assuming that a month consists of a period of 30 days; end time is offset by 30 days on each cycle of while loop
start = pd.to_datetime("2007-12-31")
end = start + timedelta(days=30)

# Initialize empty master lists to record the "ids" of the text posts selected for each Sample 1 & 2
sample1 = []
sample2 = []


# Initialize while loop with condition that start <= 2021 July 10 ie a date greater than the last published date in the database (2021 June 30)
while start <= pd.to_datetime("2021 July 10"):
    print("Processing: ", start)

    # Filter the data based on start and end dates of a given month and extract "date" and "ids"
    temp = df[(df['date'] >= start) & (df['date'] < end)]
    temp = temp[["date", "id"]]

    # Shuffle the dataframe for 1000 times to extract two random samples of the data with while loop
    shuffles = 0

    while True:
        temp = temp.sample(frac=1)
        shuffles += 1

        if shuffles > 1000:
            break

    #print("Full: ", len(temp))

    # Keep a fraction of the posts c.15.5% slightly on the higher side of the 150,000 mark for Sample 1
    samp1 = temp.sample(frac=0.155)

    # Record the posts count in sample 1 so as to match the count with sample 2
    postCount = len(samp1)

    # Filter the dataframe to exclude all the posts that have already been selected in sample 1 and extract the same number of posts for sample 2 from the rest as done for sample 1
    samp2 = temp[~temp.id.isin(samp1.id)]
    samp2 = samp2.sample(n=postCount)

    #print("Temp: ", len(samp1), len(samp2))

    # Store the ids of the posts selected for Sample 1 & 2 in two temporary lists
    l1 = samp1["id"].to_list()
    l2 = samp2["id"].to_list()

    # Append the post ids selected from a given month to the master lists initialized earlier
    sample1 = sample1 + l1
    sample2 = sample2 + l2

    print("Final: ", len(sample1), len(sample2))

    # After the processing is finished for a given month, move the "start" and "end" dates by 30 days to continue to loop/process through next month and onwards...
    start = end
    end = start + timedelta(days=30)
