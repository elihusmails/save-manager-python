from flask import Flask, jsonify, Response, make_response
import json
from collections import defaultdict
import os

from database import RedditSaverDatabase

class RestInterface:

    app = Flask(__name__)

    def __init__(self):
        self.app.run(debug=True)

    @app.route('/reddit-manager/subreddits')
    def get_subreddits():
        database = RedditSaverDatabase()
        subreddits = database.get_subreddits()
        resp = Response(json.dumps(subreddits), content_type='application/json; charset=utf-8')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

    @app.route('/reddit-manager/<subreddit>/saved')
    def get_subreddit_saved(subreddit):
        database = RedditSaverDatabase()
        retval = database.get_all_for_subreddit(subreddit)
        resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

    @app.route('/reddit-manager/message/<message>')
    def get_subreddit_message(message):
        database = RedditSaverDatabase()
        retval = database.get_subreddit_message(message)
        resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

    @app.route('/reddit-manager/subreddit/count')
    def get_subreddit_count():
        database = RedditSaverDatabase()
        retval = database.get_subreddit_msg_count()
        resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

    @app.route('/reddit-manager/posts')
    def get_posts():
        database = RedditSaverDatabase()
        retval = database.get_all_posts()
        resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

    @app.route('/reddit-manager/')
    def init():
        print('hello')

    # if __name__ == '__main__':
    #     app.run(debug=True)
