# -*- coding: utf-8 -*-

import pymongo
import tweepy
from pymongo.errors import ConnectionFailure

# key and token from twitter api
consumer_key = "YOUR CONSUMER KEY HERE"
consumer_secret = "YOUR CONSUMER SECRET HERE"
access_token = "YOUR ACCESS TOKEN HERE"
access_token_secret = "YOUT ACCESS TOKEN SECRET"

def load_twitter_api():
    """
    Creating the authentication object
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # params wait_on_rate_limit and wait_on_rate_limit_notify
    # tweepy API call auto wait (sleep) when it hits the rate limit
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def search_tweets(query, max_tweets=1000000, lang='pt'):    
    data = []
    
    api = load_twitter_api()
    tweets = tweepy.Cursor(api.search, q=query, lang=lang).items(max_tweets)

    for item in tweets:
        aux = item._json        
        data.append({
            'id': aux['id_str'],
            'username': aux['user']['screen_name'],
            'followers': aux['user']['followers_count'],
            'text': aux['text'],
            'hashtags': aux['entities']['hashtags'],
            'language': aux['lang'],
            'created_at': aux['created_at']
        })

    return data


def get_connection():        
    try:
        connection_string_local = "mongodb://localhost:27017/"    
        return pymongo.MongoClient(connection_string_local)
    except ConnectionFailure:
        print("Server not available")


def save_collections(data, connection=None):
    try:

        if not connection:
            connection = get_connection()

        # create database and create collections
        db = connection['twitterdb']
        tweets = db['tweets']

        # insert multiple documents into a collection
        resp = tweets.insert_many(data)
    except ConnectionFailure:
        print("Server not available")


def get_count_collections():
    """
    Return count collections
    """

    connection = get_connection()
    db = connection['twitterdb']
    tweets = db['tweets']
    return tweets.count()

def clean_database():
    """
    Clean all collections in database
    """        
    connection = get_connection()
    db = connection['twitterdb']
    tweets = db['tweets']
    tweets.remove({})