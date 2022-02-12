# This script was used to preprocess the text data contained within every Reddit post collected

# Import required libraries
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import re


# LOAD DATA ==>

# Create SQL engine to retrieve the data from Table "A" and "B" in reddit.db database
# First provide path of the local reddit.db file;
# path can be changed as per requirement, as if running on a different system
path = "C:/Users/Akshay/Desktop/ClimateChange/Database"

# Then initiate the SQL engine
engine = create_engine(
    f'sqlite:///{path}/reddit.db')

# Retrieve data from database into a dataframe "posts" and make it ready for preprocessing
postsA = pd.read_sql("""select * from A order by utc asc""", engine)
postsA['id'] = postsA['i'].astype(str) + "A"
postsB = pd.read_sql("""select * from B order by utc asc""", engine)
postsB['id'] = postsB['i'].astype(str) + "B"
posts = pd.concat([postsA, postsB])
posts['date'] = posts['utc'].map(
    lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
posts.set_index('date', inplace=True)
posts.sort_index(inplace=True, ascending=False)
postsA = None
postsB = None


# PREPROCESSING ==>

# Concatenate the text from "title" and "main body" of the reddit posts
posts['text'] = posts['title'] + "  " + posts['post']
print(posts.head())

# Define a list of punctuation marks that are not required for our use case
puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
          '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…',
          '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─',
          '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
          '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√']

# Function to replace punctuation marks with whitespace


def clean_text(x):
    x = str(x)
    for punct in puncts:
        if punct in x:
            x = x.replace(punct, ' ')
    return x


# Remove URL's from posts
posts['clean_text'] = posts['text'].apply(lambda x: re.sub(r'http\S+', '', x))

# Remove punctuation marks
posts['clean_text'] = posts['clean_text'].apply(lambda x: clean_text(x))

# Remove numbers
posts['clean_text'] = posts['clean_text'].str.replace("[0-9]", " ")

# Remove whitespaces
posts['clean_text'] = posts['clean_text'].apply(lambda x: ' '.join(x.split()))

# Convert text to lowercase
posts['clean_text'] = posts['clean_text'].str.lower()

# Drop duplicates
posts.drop_duplicates(['clean_text'], inplace=True)

print("Total number of unique posts: ", len(posts))
print(posts.head())

# Save a copy of the preprocessed data to be used in other scripts of the project later on
posts.to_csv("PreProcessedData.csv")
