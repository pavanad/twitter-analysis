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
    api = tweepy.API(auth)
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

def save_collections(data):
    try:
        # connect in mongoDB
        connection = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # create database and create collections
        db = connection['twitterdb']
        tweets = db['tweets']

        # insert multiple documents into a collection
        resp = tweets.insert_many(data)
        

    except ConnectionFailure:
        print("Server not available")
