"""
This module contains code for processing KDrama data.
"""

import datetime
import pandas as pd

# Load the CSV data into a pandas DataFrame and convert 'Start_date' to datetime format
df = pd.read_csv('top100_kdrama.csv')
df['Start_date'] = pd.to_datetime(df['Start_date'], errors='coerce')

# Filter rows where 'Start_date' is more recent than 01/01/2018
df2 = df[df['Start_date'] > datetime.datetime(2018, 1, 1)]

# Get a statistical summary of the data


names = df2['Main Role'].str.split(', ', expand=True).stack()
namesidx = names.index.get_level_values(0)
name_counts = names.value_counts(ascending=False)

# Get the top 4 names
top_names = name_counts.index[:4]

# Create a function to check if any of the top names is in the 'Main Role'
def contains_top_name(role):
    for name in top_names:
        if name in role:
            return True
    return False

# Apply the function to the 'Main Role' column
mask = df2['Main Role'].apply(contains_top_name)

# Create the new DataFrame
howfamous = df2[mask][['Main Role','Title','Score', 'Episodes', 'Watchers']]
for i in howfamous.index:
    role_names = howfamous.loc[i, 'Main Role'].split(', ')
    howfamous.loc[i, 'Main Role'] = ', '.join(name for name in role_names if name in top_names)
    
howfamous.set_index('Main Role', inplace=True)
print(howfamous)