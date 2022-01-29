# This script was used to run K-means clustering algorithm for k = 20 number of optimum clusters as identified by Elbow Method in the previous step
# K-means cluster labels were obtained as output corresponding to post "ids" from both Sample 1 and 2

# Import required libraries
import pandas as pd
from sklearn.cluster import KMeans


# Define a function to run K-means clustering algorithm on Sample 1 & 2
def runKMeans(sampNo=1):          # Default value of "sampNo" ie Sample No. assumed as 1

    # Load Sample 1 or 2 embeddings obtained from script "4b"
    df = pd.read_csv(f"Sample{sampNo}Embeddigs.csv")

    # Check the format of the embeddings data; identified as "str" in this case
    print(type(df["embeddings"][0]))

    # Load only 150k posts per sample for further processing due to memory constraints
    # By hit & trial it was realized that a machine with 16GB RAM could run the upcoming steps for a sample size of 150k max
    # So only kept 150k random posts per sample as per our hardware limitations
    df = df.sample(n=150000, random_state=47)

    # Convert the "str" format of the embeddings to "list" format to be used as input in clustering algorithm
    X = list(df["embeddings"].values)
    for i in range(len(X)):
        X[i] = X[i].strip('][').split(', ')

    # Check the format of the embeddings data; should be "list" in this case
    print(type(X[0]))

    # Fit the data to KMeans clustering algorithm for k = 20 ie optimum number of clusters as observed from Elbow plots in the previous steps
    kmeans = KMeans(n_clusters=20, n_jobs=-1).fit(X)

    # Store the lables to the dataframe corresponding to the respective "ids"
    df["labels"] = kmeans.labels_

    # Select the columns to be exported
    df = df[["ids", "labels"]]

    # Save the output to local disk
    df.to_csv(f"KmeansLabelsSample{sampNo}.csv", index=False)


# Run the function for Sample 1 and receive the cluster labels output file "KmeansLabelsSample1.csv" on local disk in csv format
runKMeans()

# Run the function again for Sample 2 and receive the K-means cluster labels output same as earlier
runKMeans(sampNo=2)
