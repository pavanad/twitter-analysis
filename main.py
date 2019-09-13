# -*- coding: utf-8 -*-

import json
from twitter_api import *

def main():
    
    # search tweets
    query = ['$btc', '#btc', 'btc', '$bitcoin', '#bitcoin', 'bitcoin']
    tweets = search_tweets(query)
    
    # saves to mongoDB database
    save_collections(tweets)

    # create data analysis here

if __name__ == '__main__':
    main()