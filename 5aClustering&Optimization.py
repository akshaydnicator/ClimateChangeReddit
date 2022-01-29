# This script was used to complete Step 1 of Clustering & Optimization
# ie Identifying optimum number of clusters within Sample 1 & 2 for K-means clustering algorithm using Elbow method

# Import required libraries
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Define a function to obtain Sum of Squared Errors (SSEs) for a range of number of clusters (k) for Sample 1 or 2 while running K-means algorithm
def elbowSSEs(sampNo=1):          # Default value of "sampNo" ie Sample No. assumed as 1

    # Load Sample 1 or 2 embeddings obtained from previous step
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

    # Initialiaze an empty list to store the SSEs for every value "k" to observe Elbow of the plot
    SSEs = []

    # Fit the data to KMeans clustering algorithm for a range of "ks" (1 to 100) - both ends included
    # And store the SSE value for each iteration in the SSEs list initialized above
    for k in range(1, 101):
        kmeans = KMeans(n_clusters=k, random_state=47, n_jobs=-1).fit(X)
        SSEs = SSEs + [kmeans.inertia_]
        print(k, ": ", kmeans.inertia_)

    # Once the iterations are done for a given sample return the list of SSEs
    return SSEs


# Run the function to obtain the list of SSEs for Sample 1
SSEs1 = elbowSSEs()

# Run the function to obtain the list of SSEs for Sample 2
SSEs2 = elbowSSEs(sampNo=2)

# Range of ks used
k = range(1, 101)

# Create a dataframe from the three lists obtained above
elbowData = pd.DataFrame(data={"k": k, "sample1": SSEs1, "sample2": SSEs2})

# Save the data to the local disk for further processing
elbowData.to_csv("SamplesSSEs.csv", index=False)
