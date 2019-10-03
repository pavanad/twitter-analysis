
# -*- coding: utf-8 -*-

import json
from twitter_api import *

def streaming():
    
    max_id = -1
    lang = 'pt'
    since_id = None
    tweets_per_qry = 100

    max_tweet_database = 100

    # search tweets
    query = ['$btc', '#btc', 'btc', '$bitcoin', '#bitcoin', 'bitcoin']
    
    count_tweets = 0
    api = load_twitter_api()

    print("Downloading tweets...")

    while True:
        try:
            if (max_id <= 0):
                if (not since_id):
                    tweets = api.search(q=query, lang=lang, count=tweets_per_qry)
                else:
                    tweets = api.search(q=query, lang=lang, count=tweets_per_qry, since_id=since_id)
            else:
                if (not since_id):
                    tweets = api.search(q=query, lang=lang, max_id=str(max_id - 1))
                else:   
                    tweets = api.search(q=query, lang=lang, since_id=since_id, max_id=str(max_id - 1))

            max_id = tweets[-1].id
            count_tweets += len(tweets)

            # saves to mongoDB database
            data = [t._json for t in tweets]            
            save_collections(data)

            if not tweets:
                print("No more tweets found")
                break

            if count_tweets >= max_tweet_database:
                print(f"Downloaded tweets: {count_tweets}")
                break

        except tweepy.TweepError as e:            
            print(f"Tweety error : {str(e)}")
            break

if __name__ == '__main__':
    streaming()