# This script was used to obtain Universal Setence Encoder (USE) embeddings for every preprocessed Reddit post

# Import required libraries
import pandas as pd
import tensorflow_hub as hub
import json
import numpy as np


# Load the cleaned data from "PreProcessedData.csv" file
posts = pd.read_csv("PreProcessedData.csv")
posts["date"] = pd.to_datetime(posts["date"])


# FEATURE SELECTION | Retrieve USE EMBEDDINGS for each cleaned text post ==>

# Load the latest model of pretrained USE encoder from Tensorflow Hub
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("module %s loaded" % module_url)


# Function to obtain output from the USE model for a given text input


def embed(input):
    return model(input)


# Create a list of subsets of 1000 posts each to limit the number of posts to 1000 per batch while using as an input in the USE model
list_train = [posts[i:i+1000] for i in range(0, posts.shape[0], 1000)]

# Create an empty dictionary to store the "ids" and corresponding "embeddings" ie feature vectors for each text post
data = {
    "ids": [],
    "embeddings": []
}

# Initializing the post counter and save counter to keep track of number of posts and the times the embeddings got saved on the local disk
count = 0
saved = 1


# Loop through each batch of 1000 posts to obtain embeddings from USE model
for i in range(len(list_train)):

    # Obtain embeddings for the batch
    embeddings = embed(list_train[i]['clean_text'])

    # Store the ids and corresponding embeddings obtained from USE model in the "data" dictionary
    data['ids'].extend(list_train[i]['id'].values.tolist())
    data['embeddings'].extend(np.array(embeddings).tolist())

    count += len(list_train[i])

    # To track the progress
    if count in [25000, 50000, 75000]:
        print(f"Posts count: {count}")

    # Save the "data" in json format on local disk everytime the post count equals or exceeds 100,000 mark
    # As the size of the feature vectors is huge, the count was limited to 100k per file to make it manageable in terms of data loading and processing
    if count >= 100000:

        # Save the data in a json file. Data can be converted to any other format ie csv, tsv etc later.
        with open(f"Embeddings{saved}", "w") as fp:
            json.dump(data, fp, indent=4)

        # Initialiaze the post count to 0 and increased the number of times saved by 1
        count = 0
        saved += 1

        # Initialize the data dictionary again to start storing the new embeddings from the list_train dataframes
        data = {
            "ids": [],
            "embeddings": []
        }

        print(f"Saved File {saved}.. Count of Posts {round(i/1000,3)} m")


# Save the last leg of data with count < 100k, which could not be saved in the "for" loop above
with open(f"Embeddings{saved}", "w") as fp:
    json.dump(data, fp, indent=4)
