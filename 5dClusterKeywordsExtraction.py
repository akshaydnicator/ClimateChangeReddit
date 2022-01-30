# This script was used to extract underlying keywords from various clusters within Sample 1 and 2
# The aim here is to compare and analyze the keywords across clusters and merge/optimize the number of clusters (k) further based on observation/domain knowlegde

# Import required libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import time
from datetime import timedelta


# Load the cleaned data from "PreProcessedData.csv" file
posts = pd.read_csv("PreProcessedData.csv")
posts["date"] = pd.to_datetime(posts["date"])

# Provide ngram_range parameter input for Countvectorizer
ngramRange = [1, 2]


# Define a function to extract the list of keywords for every cluster in Sample 1 & 2, and save it on the local disk for further analysis
# Default value of "sampNo" ie Sample No. assumed as 1
def extractKeywords(sampNo=1):

    # Load the post ids and cluster labels data obtained from previous step
    sample = pd.read_csv(f"KmeansLabelsSample{sampNo}.csv")

    # Filter the cleaned data based on sample ids and merge the labels to the dataframe
    sampledf = posts[posts["id"].isin(sample["ids"].values)].copy()
    sampledf = sampledf.merge(
        sample, how='inner', left_on='id', right_on='ids')

    # Check the length of the dataframe; it should be 150,000 in this case
    print(len(sampledf))

    # Instantiate an Excel writer to save the list of extracted keywords in an excel file for each sample
    writer = pd.ExcelWriter(
        f"ClusterKeywordsSample{sampNo}.xlsx", engine='xlsxwriter')

    # Record the time at the beginning of for loop
    start = time.monotonic()

    # Loop through all of the 20 clusters obtained for each sample and save the keywords & count in a new sheet in excel workbook
    for i in range(20):

        # Filter the posts data based on Cluster No.
        temp = sampledf[sampledf["labels"] == i].copy()

        # Run the countvectorizer for ngramRange provided
        for j in ngramRange:

            # ngram_range (1,2) used to check all the keywords (max bigrams) with mentions >= 100
            # ngram_range (2,2) used to check all the bigrams with mentions >= 50
            cv = CountVectorizer(ngram_range=(j, 2), stop_words='english')

            # Fit the cleaned data
            cvFit = cv.fit_transform([str(temp['clean_text'].values.tolist())])

            # Obtain list of keywords and their respective count
            wordList = cv.get_feature_names()
            countList = cvFit.toarray().sum(axis=0)

            dictionary = dict(zip(wordList, countList))
            dictionary = dict(
                sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

            cvDf = pd.DataFrame(list(dictionary.items()), columns=[
                                f'keywords_{i}', f'count_{i}'])

            # Provide the word count limit and naming prop to save the output in a new excel sheet per cycle
            if j == 1:
                limit = 100
                sheet = ""
            else:
                limit = 50
                sheet = "a"

            # Save the output in a new excel sheet
            cvDf[cvDf[f'count_{i}'] >= limit].to_excel(
                writer, sheet_name=f'Cluster{i}{sheet}', index=False)

    # Observe the time it took to complete the for loop for a given sample
    end = time.monotonic()
    print(f"Done! Total time taken: {timedelta(seconds=(end-start))}")

    # Save the final updated excel file on local disk
    writer.save()


# Run the function for Sample 1
extractKeywords()

# Run the function for Sample 2
extractKeywords(sampNo=2)
