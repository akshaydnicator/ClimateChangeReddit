# This script was used to obtain 2 UMAP components for 512D sample USE embeddings for visualizing the final clusters in a 2D space

# Import required libraries
import pandas as pd
import umap


# Define a function to run UMAP algorithm on Sample 1 & 2
def runUMAP(sampNo=1):          # Default value of "sampNo" ie Sample No. assumed as 1

    # Load Sample 1 or 2 embeddings obtained from script "4b"
    df = pd.read_csv(f"Sample{sampNo}Embeddigs.csv")

    # Check the format of the embeddings data; identified as "str" in this case
    print(type(df["embeddings"][0]))

    # Load only 150k posts per sample for further processing due to memory constraints
    # By hit & trial it was realized that a machine with 16GB RAM could run the upcoming steps for a sample size of 150k max
    # So only kept 150k random posts per sample as per our hardware limitations
    df = df.sample(n=150000, random_state=47)

    # Convert the "str" format of the embeddings to "list" format to be used as an input in the model
    X = list(df["embeddings"].values)
    for i in range(len(X)):
        X[i] = X[i].strip('][').split(', ')

    # Check the format of the embeddings data; should be "list" in this case
    print(type(X[0]))

    # Fit the data to UMAP model to obtain 2 components reprensenting 512D embeddings in a 2D space
    embedding = umap.UMAP(n_neighbors=50, verbose=True,
                          low_memory=True, n_jobs=-1, n_epochs=2000).fit_transform(X)

    # Add the two UMAP components to the dataframe
    df["UMAPx"] = embedding[:, 0]
    df["UMAPy"] = embedding[:, 1]

    # Select the columns to be exported
    df = df[["ids", "UMAPx", "UMAPy"]]

    # Save the output to local disk
    df.to_csv(f"UMAPComponentsSample{sampNo}.csv", index=False)


# Run the function for Sample 1 and receive the 2 UMAP components in the output file "UMAPComponentsSample1.csv" on local disk in csv format
runUMAP()

# Run the function again for Sample 2 and receive the 2 UMAP components in the output file "UMAPComponentsSample2.csv"
runUMAP(sampNo=2)
