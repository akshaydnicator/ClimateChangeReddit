# This script was used to create monthly time series of proportion of subclusters within Energy (Cluster 1)

# Import required libraries
import pandas as pd

# Read the preprocessed data in a dataframe
df = pd.read_csv("PreProcessedData.csv", usecols=["date", "id"])


# Function to create the monthly time series for the proportion of Energy subclusters
def calEnergySubclustersProp(sampNo=1):      # Default value of Sample = 1

    sample = pd.read_csv(f"kmeansLabelsSample{sampNo}.csv")

    if sampNo == 1:
        labels = [0, 10, 14, 17, 19]
        keys = {
            0: "EVs/Alternative fuels",
            10: "Solar energy",
            14: "Renewable energy",
            17: "Nuclear energy",
            19: "Oil & gas"
        }

    else:
        labels = [2, 11, 0, 8, 18]
        keys = {
            2: "EVs/Alternative fuels",
            11: "Solar energy",
            0: "Renewable energy",
            8: "Nuclear energy",
            18: "Oil & gas"
        }

    temp = df.merge(sample, how='inner', left_on='id', right_on='ids')
    temp['date'] = pd.to_datetime(temp['date'])
    temp.set_index('date', inplace=True)
    print(len(temp))

    temp = temp[temp.labels.isin(labels)].copy()

    totalCount = temp.resample("M").count()
    TSdf = totalCount[['id']].copy()
    TSdf.rename(columns={'id': 'Total'}, inplace=True)

    for i in labels:

        clusterdf = temp[temp.labels == i].copy()

        countdf = clusterdf.resample("M").count()
        TSdf = TSdf.join(countdf['id'])
        TSdf.rename(columns={'id': f'{keys[i]}'}, inplace=True)

    for i in labels:
        TSdf[f'pr-{keys[i]}'] = TSdf[f'{keys[i]}']/TSdf['Total']
        TSdf.to_csv(f"Sample{sampNo}EnergySubClustersProportion.csv")


# Obtain the time series for Sample 1 & 2
calEnergySubclustersProp()
calEnergySubclustersProp(sampNo=2)
