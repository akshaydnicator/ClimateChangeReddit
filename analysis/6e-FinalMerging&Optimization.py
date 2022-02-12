# This script was used to merge and further optimize the number of Clusters based on underlying keywords and domain knowledge
# The optimum clusters, obtained after applying the Elbow method in scripts "5a, 5b & 5c", were further merged and their number was reduced from 20 to 12

# Import required libraries
import pandas as pd


# SAMPLE 1 relabeling for 12 Optimized Clusters
df = pd.read_csv("KmeansLabelsSample1.csv")

df.loc[df['labels'] == 0, ['labels']] = 41
df.loc[df['labels'] == 10, ['labels']] = 41
df.loc[df['labels'] == 14, ['labels']] = 41
df.loc[df['labels'] == 17, ['labels']] = 41
df.loc[df['labels'] == 19, ['labels']] = 41
df.loc[df['labels'] == 8, ['labels']] = 42
df.loc[df['labels'] == 4, ['labels']] = 43
df.loc[df['labels'] == 12, ['labels']] = 44
df.loc[df['labels'] == 5, ['labels']] = 45
df.loc[df['labels'] == 11, ['labels']] = 46
df.loc[df['labels'] == 7, ['labels']] = 47
df.loc[df['labels'] == 3, ['labels']] = 48
df.loc[df['labels'] == 9, ['labels']] = 49
df.loc[df['labels'] == 15, ['labels']] = 49
df.loc[df['labels'] == 16, ['labels']] = 49
df.loc[df['labels'] == 18, ['labels']] = 50
df.loc[df['labels'] == 1, ['labels']] = 51
df.loc[df['labels'] == 6, ['labels']] = 51
df.loc[df['labels'] == 13, ['labels']] = 51
df.loc[df['labels'] == 2, ['labels']] = 52

df.loc[df['labels'] == 41, ['labels']] = 1
df.loc[df['labels'] == 42, ['labels']] = 2
df.loc[df['labels'] == 43, ['labels']] = 3
df.loc[df['labels'] == 44, ['labels']] = 4
df.loc[df['labels'] == 45, ['labels']] = 5
df.loc[df['labels'] == 46, ['labels']] = 6
df.loc[df['labels'] == 47, ['labels']] = 7
df.loc[df['labels'] == 48, ['labels']] = 8
df.loc[df['labels'] == 49, ['labels']] = 9
df.loc[df['labels'] == 50, ['labels']] = 10
df.loc[df['labels'] == 51, ['labels']] = 11
df.loc[df['labels'] == 52, ['labels']] = 12

# Check the labels and their respective counts to confirm the correct changes for sample 1
print(df['labels'].value_counts())

# Save the Final cluster labels to the local disk
df.to_csv("FinalLabelsSample1.csv", index=False)


# SAMPLE 2 relabeling for 12 Optimized Clusters
df = pd.read_csv("KmeansLabelsSample2.csv")

# Sort Sample 2 labels w.r.t. Sample 1
# As the order of similar clusters is different within Sample 1 & 2, reorder the Sample 2 labels to match with Sample 1 (for input purposes in later scripts)
df.loc[df['labels'] == 2, ['labels']] = 40
df.loc[df['labels'] == 13, ['labels']] = 41
df.loc[df['labels'] == 17, ['labels']] = 42
df.loc[df['labels'] == 9, ['labels']] = 43
df.loc[df['labels'] == 14, ['labels']] = 44
df.loc[df['labels'] == 5, ['labels']] = 45
df.loc[df['labels'] == 16, ['labels']] = 46
df.loc[df['labels'] == 7, ['labels']] = 47
df.loc[df['labels'] == 1, ['labels']] = 48
df.loc[df['labels'] == 12, ['labels']] = 49
df.loc[df['labels'] == 11, ['labels']] = 50
df.loc[df['labels'] == 19, ['labels']] = 51
df.loc[df['labels'] == 15, ['labels']] = 52
df.loc[df['labels'] == 4, ['labels']] = 53
df.loc[df['labels'] == 0, ['labels']] = 54
df.loc[df['labels'] == 10, ['labels']] = 55
df.loc[df['labels'] == 6, ['labels']] = 56
df.loc[df['labels'] == 8, ['labels']] = 57
df.loc[df['labels'] == 3, ['labels']] = 58
df.loc[df['labels'] == 18, ['labels']] = 59

df.loc[df['labels'] == 40, ['labels']] = 0
df.loc[df['labels'] == 41, ['labels']] = 1
df.loc[df['labels'] == 42, ['labels']] = 2
df.loc[df['labels'] == 43, ['labels']] = 3
df.loc[df['labels'] == 44, ['labels']] = 4
df.loc[df['labels'] == 45, ['labels']] = 5
df.loc[df['labels'] == 46, ['labels']] = 6
df.loc[df['labels'] == 47, ['labels']] = 7
df.loc[df['labels'] == 48, ['labels']] = 8
df.loc[df['labels'] == 49, ['labels']] = 9
df.loc[df['labels'] == 50, ['labels']] = 10
df.loc[df['labels'] == 51, ['labels']] = 11
df.loc[df['labels'] == 52, ['labels']] = 12
df.loc[df['labels'] == 53, ['labels']] = 13
df.loc[df['labels'] == 54, ['labels']] = 14
df.loc[df['labels'] == 55, ['labels']] = 15
df.loc[df['labels'] == 56, ['labels']] = 16
df.loc[df['labels'] == 57, ['labels']] = 17
df.loc[df['labels'] == 58, ['labels']] = 18
df.loc[df['labels'] == 59, ['labels']] = 19

# Once the order is corrected, relabel the clusters for sample 2
df.loc[df['labels'] == 0, ['labels']] = 41
df.loc[df['labels'] == 2, ['labels']] = 41
df.loc[df['labels'] == 8, ['labels']] = 41
df.loc[df['labels'] == 11, ['labels']] = 41
df.loc[df['labels'] == 18, ['labels']] = 41
df.loc[df['labels'] == 1, ['labels']] = 42
df.loc[df['labels'] == 14, ['labels']] = 43
df.loc[df['labels'] == 15, ['labels']] = 44
df.loc[df['labels'] == 5, ['labels']] = 45
df.loc[df['labels'] == 19, ['labels']] = 46
df.loc[df['labels'] == 7, ['labels']] = 47
df.loc[df['labels'] == 16, ['labels']] = 48
df.loc[df['labels'] == 6, ['labels']] = 49
df.loc[df['labels'] == 10, ['labels']] = 49
df.loc[df['labels'] == 12, ['labels']] = 49
df.loc[df['labels'] == 3, ['labels']] = 50
df.loc[df['labels'] == 4, ['labels']] = 51
df.loc[df['labels'] == 9, ['labels']] = 51
df.loc[df['labels'] == 13, ['labels']] = 51
df.loc[df['labels'] == 17, ['labels']] = 52

df.loc[df['labels'] == 41, ['labels']] = 1
df.loc[df['labels'] == 42, ['labels']] = 2
df.loc[df['labels'] == 43, ['labels']] = 3
df.loc[df['labels'] == 44, ['labels']] = 4
df.loc[df['labels'] == 45, ['labels']] = 5
df.loc[df['labels'] == 46, ['labels']] = 6
df.loc[df['labels'] == 47, ['labels']] = 7
df.loc[df['labels'] == 48, ['labels']] = 8
df.loc[df['labels'] == 49, ['labels']] = 9
df.loc[df['labels'] == 50, ['labels']] = 10
df.loc[df['labels'] == 51, ['labels']] = 11
df.loc[df['labels'] == 52, ['labels']] = 12

# Check the labels and their respective counts to confirm the correct changes for sample 2
print(df['labels'].value_counts())

# Save the Final cluster labels to the local disk
df.to_csv("FinalLabelsSample2.csv", index=False)
