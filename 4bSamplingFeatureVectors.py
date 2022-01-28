# This script was used to obtain "USE Embeddings" ie Feature vectors for posts in Sample 1 and 2 corresponding to the post "IDs" collected in previous script

# Import required libraries
import pandas as pd


# Load sample ids selected from previous step into a dataframe and check the contents
samples = pd.read_csv("samples.csv")
print(samples.head())

# Crate a separate list of ids for each sample
sample1 = list(samples["sample1"].values)
sample2 = list(samples["sample2"].values)

# Initialize empty dataframes to store sample "ids" and corresponding post "embeddings" for future processing
samp1Embed = pd.DataFrame()
samp2Embed = pd.DataFrame()


# As there were 16 files that were stored on local disk from Step 3, loop through each one of them to filter the sample embeddings and store in the dataframes initialized above
# For the sake of saving disk space, the Embeddings files in .json format from Step 3 were converted into .csv format and used as input below
for i in range(1, 17):
    df = pd.read_csv(f"Embeddings{i}.csv")

    temp1 = df[df.ids.isin(sample1)]
    temp2 = df[df.ids.isin(sample2)]

    samp1Embed = samp1Embed.append(temp1)
    samp2Embed = samp2Embed.append(temp2)

    print(len(samp1Embed), len(samp2Embed))

# After looping through all the files, save the final sample 1 & 2 dataframes with "ids" and corresponding "embeddings" of the posts to the local disk
samp1Embed.to_csv("Sample1Embeddigs.csv", index=False)
samp2Embed.to_csv("Sample2Embeddigs.csv", index=False)
