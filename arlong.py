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

# Now filter the DataFrame
df2 = df[df['Start_date'] > datetime.datetime(2018, 1, 1)]

# Processing names
names = df2['Main Role'].str.split(', ', expand=True).stack()
name_counts = names.value_counts(ascending=False)

# Get the top 4 names
top_names = name_counts.index[:4].tolist()

# Create a function to check if any of the top names is in the 'Main Role'
def contains_top_name(role):
    return any(name in role for name in top_names)

def truncate_label(label, max_length):
    """Truncate a label to a maximum length with an ellipsis."""
    if len(label) > max_length:
        return label[:max_length - 3] + '...'
    return label

max_label_length = 25
# Apply the function to the 'Main Role' column
df2 = df2[df2['Main Role'].apply(contains_top_name)]
df2['Main Role'] = df2['Main Role'].apply(lambda x: ', '.join(name for name in x.split(', ') if name in top_names))

# Group and sort the data
grouped_dfs = {name: df2[df2['Main Role'].str.contains(name)] for name in top_names}

df2['Title'] = df2['Title'].replace(title_mapping)


fig, axs = plt.subplots(2, 2, figsize=(16, 8))
axs = axs.flatten()

# Define a list of colors
colors = ['Salmon', 'Green', 'Pink', 'purple']

# Plot each grouped DataFrame
for i, (name, group_df) in enumerate(grouped_dfs.items()):
    # Truncate y-axis labels
    truncated_titles = group_df['Title'].apply(lambda x: truncate_label(x, max_label_length))
    
    sns.barplot(x=group_df['Score'], y=truncated_titles, color=colors[i], ax=axs[i])
    axs[i].set_title(name, fontsize=20)
    axs[i].set_xlabel('Score', fontsize=15)
    axs[i].set_ylabel('Title', fontsize=15)
    axs[i].set_xlim(8.5, 10)
    axs[i].xaxis.set_major_locator(plt.MaxNLocator(6))

# Adjust the layout and save the plot
plt.tight_layout()
plt.savefig('All_Plots.png', bbox_inches='tight')