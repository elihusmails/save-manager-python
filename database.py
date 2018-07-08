import os
import sqlite3
import json

class RedditSaverDatabase:

    db_filename = 'reddits.db'
    schema_filename = 'schema.sql'

    def __init__(self):
        db_is_new = not os.path.exists(self.db_filename)

        with sqlite3.connect(self.db_filename) as conn:
            if db_is_new:
                print('Creating schema')
                with open(self.schema_filename, 'rt') as f:
                    schema = f.read()
                conn.executescript(schema)


    def get_all( self ):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM redditsaves')

            retval = []

            for row in cursor.fetchall():
                rid, title, permalink, subreddit = row 
                retval.append( {'_id': rid,
                    'title': title,
                    'permalink': permalink,
                    'subreddit': subreddit} )

            return retval

    def get_subreddits( self ):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT distinct(subreddit) FROM redditsaves')
            retval = []
            for row in cursor:
                subreddit = row
                retval.append(subreddit)

            return retval

    def get_all_for_subreddit( self, subreddit ):
         with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM redditsaves WHERE subreddit = ?', (subreddit,))
            retval = []
            for row in cursor.fetchall():
                rid, title, permalink, subreddit = row 
                retval.append( {'_id': rid,
                    'title': title,
                    'permalink': permalink,
                    'subreddit': subreddit} )

            return retval

    def get_subreddit_message( self, msgid ):
         with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM redditsaves WHERE reddit_id = ?', (msgid,))
            retval = []
            for row in cursor.fetchall():
                rid, title, permalink, subreddit = row 
                retval.append( {'_id': rid,
                    'title': title,
                    'permalink': permalink,
                    'subreddit': subreddit} )

            return retval

    def get_subreddit_msg_count( self ):
          with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT subreddit, COUNT(*) AS count FROM redditsaves GROUP BY subreddit')
            retval = []
            for row in cursor.fetchall():
                subreddit,count = row 
                retval.append( {
                    'subreddit': subreddit,
                    'count': count
                    } )

            return retval       

    def get_all_posts( self ):

        retval = {}
        retval['name'] = 'flare'
        flareChildren = []

        subreddits = self.get_subreddits()
        for subreddit in subreddits:
            with sqlite3.connect(self.db_filename) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT title,permalink FROM redditsaves WHERE subreddit = ?', subreddit)
                srObj = {}
                srObj['name'] = subreddit[0]
                children = []
                for row in cursor.fetchall():
                    title, permalink = row 
                    children.append( {'name':title, 'permalink':permalink} )
                srObj['children'] = children
                flareChildren.append(srObj)
                
        retval['children'] = flareChildren
        return retval         

    def insert_saved_thing( self, id, subreddit, title, permalink ):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT reddit_id FROM redditsaves WHERE reddit_id = ?', (id,))
            data = cursor.fetchone()
            if data is None:
                print('There is no record named %s' % id)

                cursor.execute('INSERT INTO redditsaves (reddit_id, title, permalink, subreddit) VALUES (:id,:title,:permalink,:subreddit)', 
                {'id':id, 'title':title, 'permalink':permalink, 'subreddit':subreddit})


