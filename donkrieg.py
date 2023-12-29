''' This script is used to visualize the data from the redditdata.csv file. It creates a heatmap of the comment scores on the KDRAMA subreddit. '''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

redditdata = pd.read_csv('C:/Users/ludoz/OneDrive/Documents/GitHub/East-blue/redditdata.csv')
redditdata_subset1 = pd.DataFrame(redditdata)

redditdata_subset1['post_title'] = redditdata_subset1['post_title'].str.wrap(30)
redditdata_subset1['comment_body'] = redditdata_subset1['comment_body'].str.wrap(30)
redditdata_subset1['post_title'] = redditdata_subset1['post_title'].str.slice(0, 100)
redditdata_subset1['comment_body'] = redditdata_subset1['comment_body'].str.slice(0, 100)
redditdata_subset1 = redditdata_subset1.pivot(index="comment_body", columns="post_title", values="comment_score")

plt.figure(figsize=(30,30))

plt.title('Heatmap of comment scores on KDRAMA subreddit')
sns.set(style="darkgrid", font_scale=1.2)

donkrieg = sns.heatmap(redditdata_subset1, annot=True, cmap="coolwarm", fmt='.1f', linewidths=.5, annot_kws={"size": 10})
plt.savefig('C:/Users/ludoz/OneDrive/Documents/GitHub/East-blue/donkrieg.png',format='png', dpi=300, bbox_inches='tight')