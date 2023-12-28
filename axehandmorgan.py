'''to correct the dates and names of the actors in the top 100 kdrama list'''
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV data into a pandas DataFrame and convert 'Start_date' to datetime format
df = pd.read_csv('top100_kdrama.csv')
# Define a dictionary to map old titles to new ones
title_mapping = {
    'Alchemy of Souls Season 2: Light and Shadow ': 'Alchemy of S2',
    'Missing: The Other Side ': 'Missing: TOS',
    'Missing: The Other Side Season 2 ': 'Missing: TOS S2',
    'Arthdal Chronicles Part 2: The Sky Turning Inside Out, Rising Land': 'Arthdal Chronicles S2',
    'Arthdal Chronicles Part 3: The Prelude to All Legends ': 'Arthdal Chronicles S3'
}

# Use the replace function to replace the titles
df['Title'] = df['Title'].replace(title_mapping)
df['Start_date'] = pd.to_datetime(df['Start_date'], errors='coerce')

# Remove common non-numeric characters (e.g., commas, alphabets)
df['Watchers'] = df['Watchers'].str.replace(',', '').str.replace(' viewers', '')
# Strip leading/trailing whitespace
df['Watchers'] = df['Watchers'].str.strip()
# Convert to numeric values
df['Watchers'] = pd.to_numeric(df['Watchers'], errors='coerce')

# Now filter the DataFrame
df2 = df[df['Start_date'] > datetime.datetime(2018, 1, 1)]

# Processing names
names = df2['Main Role'].str.split(', ', expand=True).stack()
name_counts = names.value_counts(ascending=False)

# Get the top 4 names
top_names = name_counts.index[:4].tolist()

def contains_top_name(role):
    '''Check if any of the top names is in the given role.'''
    return any(name in role for name in top_names)
# Apply the function to the 'Main Role' column
df2 = df2[df2['Main Role'].apply(contains_top_name)]
df2['Main Role'] = df2['Main Role'].apply(lambda x: ', '.join(
    name for name in x.split(', ') if name in top_names))

# Group and sort the data
grouped_dfs = {name: df2[df2['Main Role'].str.contains(name)] for name in top_names}
grouped = pd.concat(grouped_dfs.values(), keys=grouped_dfs.keys(), axis=0)
grouped.set_index('Main Role', inplace=True)
ldh = grouped.loc['Lee Do Hyun']
sjk = grouped.loc['Song Joong Ki']
onr = grouped.loc['Oh Na Ra']
lje = grouped.loc['Lee Jung Eun']
###################################################


#plot Title vs Score for each actor

fig, axs = plt.subplots(2, 2, figsize=(16, 8))
axs = axs.flatten()

colors = ['Salmon', 'Green', 'Pink', 'purple']

for i, (name, group_df) in enumerate(grouped_dfs.items()):
    sns.barplot(y=group_df['Score'], x=group_df['Title'], color=colors[i], ax=axs[i])
    axs[i].set_ylabel('Score', fontsize=15)
    axs[i].set_xlabel('Title', fontsize=15)
    axs[i].set_title(name, fontsize=20)
    axs[i].set_ylim(8.5, 10)
    axs[i].yaxis.set_major_locator(plt.MaxNLocator(6))

plt.tight_layout()
plt.savefig('Score_vs_Title.png', bbox_inches='tight')

###################################################

# Plot Title vs Watchers for each actor
fig, axs = plt.subplots(2, 2, figsize=(16, 8))
axs = axs.flatten()

colors = ['Salmon', 'Green', 'Pink', 'purple']

for i, (name, group_df) in enumerate(grouped_dfs.items()):
    # Sort the group_df by 'Watchers' in descending order for consistent ordering
    sorted_group_df = group_df.sort_values(by='Watchers', ascending=True)
    sns.barplot(y=sorted_group_df['Watchers'], x=group_df['Title'], color=colors[i], ax=axs[i])
    axs[i].set_ylabel('Audience', fontsize=15)
    axs[i].set_xlabel('Title', fontsize=15)
    axs[i].set_title(name, fontsize=20)
    axs[i].set_ylim(0, 120000)
    axs[i].yaxis.set_major_locator(plt.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig('Sorted_Watchers_vs_Title.png', bbox_inches='tight')

#####################################################
