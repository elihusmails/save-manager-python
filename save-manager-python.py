from flask import Flask, jsonify, Response, make_response
from flask_pymongo import PyMongo
import json
from collections import defaultdict

import os

app = Flask(__name__)

app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'reddit'

mongo = PyMongo(app)

@app.route('/reddit-manager/subreddits')
def get_subreddits():
    subreddits = mongo.db.messages.find().distinct('subreddit')
    resp = Response(json.dumps(subreddits), content_type='application/json; charset=utf-8')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp;

@app.route('/reddit-manager/<subreddit>/saved')
def get_subreddit_saved(subreddit):
    msgs = mongo.db.messages.find( {'subreddit':subreddit} )
    retval = []
    for doc in msgs:
        retval.append( {'_id': doc['_id'],
                        'title': doc['title'],
                        'permalink': doc['permalink'],
                        'subreddit': doc['subreddit']} )

    resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp;

@app.route('/reddit-manager/message/<message>')
def get_subreddit_message(message):
    msgs = mongo.db.messages.find({'_id': message})
    retval = []
    for doc in msgs:
        retval.append( {'_id': doc['_id'],
                        'title': doc['title'],
                        'permalink': doc['permalink'],
                        'subreddit': doc['subreddit']} )

    resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp;

@app.route('/reddit-manager/subreddit/count')
def get_subreddit_count():
    retval = []
    counts = mongo.db.messages.aggregate([ {'$unwind': '$subreddit' }, {'$group': {'_id': {'$toLower': '$subreddit'},'count': {'$sum': 1 }}}, {'$sort' : { 'count' : -1}} ])
    for doc in counts:
        retval.append( {'count':doc['count'],'_id':doc['_id']} )

    resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp;

@app.route('/reddit-manager/posts')
def get_posts():
    retval = {}
    retval['name'] = 'flare'
    flareChildren = []

    results = mongo.db.messages.aggregate( [ { '$group' : { '_id' : '$subreddit', 'children': { '$push': {'name': '$title', 'permalink': '$permalink' } } } } ] )
    for result in results :
        flareChildren.append( {'name': result['_id'], 'children': result['children']} )

    retval['children'] = flareChildren

    resp = Response(json.dumps(retval), content_type='application/json; charset=utf-8')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp;

@app.route('/reddit-manager/')
def init():
    print 'hello'

if __name__ == '__main__':
    app.run(debug=True)
