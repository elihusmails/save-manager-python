
-- Schema for storing reddit data in an SQLite3 database

-- table to store saved reddit information
create table redditsaves (
    id          integer primary key autoincrement not null,
    reddit_id   text, 
    title       text,
    permalink   text,
    subreddit   text
);