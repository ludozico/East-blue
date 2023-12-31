"""
This module provides functionality for working with CSV files.
"""
import csv
import praw

# Your Reddit script application credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = 'LUDOZICO'

# Initialize the PRAW Reddit client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Define the subreddit and the number of posts to retrieve
SUBREDDIT_NAME = 'KDRAMA'  # Change to the subreddit you want to scrape
LIMIT_POSTS = 7

# Access the subreddit
subreddit = reddit.subreddit(SUBREDDIT_NAME)

# File to save the scraped data
CSV_FILENAME = r'C:\Users\ludoz\OneDrive\Documents\GitHub\East-blue\redditdata.csv'

# The headers for the CSV file should be changed to remove 'comment_upvotes' and 'comment_downvotes'
headers = ['post_title', 'post_url', 'post_upvotes', 'comment_body', 'comment_score']

# Open the file and write the headers
with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)

    # Retrieve top posts of the last month
    top_posts = subreddit.top(time_filter='month', limit=LIMIT_POSTS)

    # Fetch top comments for each post
    for submission in top_posts:
        # Reddit doesn't load all comments by default, you must explicitly ask for more
        submission.comment_sort = 'top'  # sort by top comments
        submission.comments.replace_more(
            limit=0
        )  # This line is necessary to get all top-level comments

        # Filter out comments that start with '**Mod Note**'
        filtered_comments = [
            comment
            for comment in submission.comments.list()
            if not comment.body.startswith('**Mod Note**')
        ]

        # Get the top 3 comments, excluding those that start with '**Mod Note**'
        top_comments = filtered_comments[:3]

        for comment in top_comments:
            # Write the data to the CSV file with the available information (no upvote ratio for comments)
            csvwriter.writerow([
                submission.title,
                submission.url,
                submission.score,
                comment.body,
                comment.score,
            ])

# Let the user know the data has been saved
print(f"Data saved to {CSV_FILENAME}\n")
