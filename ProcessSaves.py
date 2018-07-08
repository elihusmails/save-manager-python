import praw
import os, sys
from database import RedditSaverDatabase

class ProcessSaves:

    configProfile = ''

    def __init__(self, configProfile):
        print('Initializing the ProcessSaves class')
        self.configProfile = configProfile


    def process_saves(self):
        reddit = praw.Reddit(self.configProfile, user_agent='RedditSaveManager:v1.0 by /u/elihusmails')
        saves = reddit.redditor(reddit.config.username).saved(limit=None)

        database = RedditSaverDatabase()

        for save in saves:

            if hasattr(save, 'title'):
                database.insert_saved_thing(save.id, save.subreddit.display_name, save.title, save.permalink)
            else:
                # submissions that get here are links to comments
                database.insert_saved_thing(save.id, save.subreddit.display_name, save.link_title, save.submission.permalink)

