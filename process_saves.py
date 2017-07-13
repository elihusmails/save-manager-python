import praw
import praw.errors
import os, sys

from pymongo import MongoClient

if __name__ == '__main__':
    user = sys.argv[0]

    reddit = praw.Reddit('bot1', user_agent='RedditSaveManager:v1.0 by /u/elihusmails')

    saves = reddit.redditor(user).saved(limit=None)

    client = MongoClient()
    db = client.reddit

    for save in saves:

        if hasattr(save, 'title'):
            record = {
                "_id": save.id,
                "subreddit": save.subreddit.display_name,
                "title": save.title,
                "permalink": save.permalink
            }

            db.messages.update({"_id":save.id}, {'$set':record}, upsert=True)
        else:
            # submissions that get here are links to comments
            record = {
                "_id": save.id,
                "subreddit": save.subreddit.display_name,
                "title": save.link_title,
                "permalink": save.submission.permalink
            }

            db.messages.update({"_id": save.id}, {'$set': record}, upsert=True)

