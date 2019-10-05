
# -*- coding: utf-8 -*-

import json
from twitter_api import *

def streaming():
    
    max_id = -1
    lang = 'en'
    result_type = 'mixed'
    since_id = None
    tweets_per_qry = 100

    max_tweet_database = 10000

    # search tweets
    query = ['$btc', '#btc', 'btc', '$bitcoin', '#bitcoin', 'bitcoin']
    
    count_tweets = 0
    api = load_twitter_api()

    # connect in mongoDB
    connection = get_connection()
    print("Connect in mongoDB")

    print("Downloading tweets...")

    while True:
        try:
            if (max_id <= 0):
                if (not since_id):
                    tweets = api.search(q=query, lang=lang, count=tweets_per_qry, result_type=result_type)
                else:
                    tweets = api.search(q=query, lang=lang, count=tweets_per_qry, since_id=since_id, result_type=result_type)
            else:
                if (not since_id):
                    tweets = api.search(q=query, lang=lang, max_id=str(max_id - 1), result_type=result_type)
                else:   
                    tweets = api.search(q=query, lang=lang, since_id=since_id, max_id=str(max_id - 1), result_type=result_type)

            count_tweets += len(tweets)
            print("", end = ".")

            if not tweets:                
                print("\nNo more tweets found")
                break

            if count_tweets >= max_tweet_database:
                print(f"Downloaded tweets: {count_tweets}")
                break

            # saves to mongoDB database
            data = [t._json for t in tweets]            
            if len(data) > 0:
                save_collections(data, connection)

            max_id = tweets[-1].id

        except tweepy.TweepError as e:            
            print(f"Tweety error : {str(e)}")
            break

if __name__ == '__main__':
    streaming()
