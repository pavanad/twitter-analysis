
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob

from twitter_api import *
from utils import remove_url


def get_tweets():    
    # connect in mongoDB
    connection = get_connection()
    print("Connect in mongoDB")

    # get database and select tweets
    db = connection["twitterdb"]
    tweets = db.tweets.find({})

    tweets_no_urls = [remove_url(tweet["text"]) for tweet in tweets]

    return tweets_no_urls


def get_tweets_setiment_hist(tweets):
    # Create textblob objects of the tweets
    sentiment_objects = [TextBlob(tweet) for tweet in tweets]

    # Create list of polarity valuesx and tweet text
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

    # Create dataframe containing the polarity value and tweet text
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
    sentiment_df.head()

    return sentiment_df

def plot_sentiment_hist(df):
    # Remove polarity values equal to zero
    sentiment_df = df[df.polarity != 0]
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot histogram with break at zero
    sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1],
                ax=ax,
                color="purple")

    plt.title("Análise de sentimentos de tweets de hastags relacionadas a #bitcoin")
    plt.xlabel("Polaridate")
    plt.ylabel("Quantidate")
    plt.show()


if __name__ == '__main__':
    tweets = get_tweets()
    print(f"Tweets: {len(tweets)}")

    sentiment = get_tweets_setiment_hist(tweets)
    print("-POLARITY - é um valor contínuo que varia de -1.0 a 1.0, sendo -1.0 referente a 100% negativo e 1.0 a 100% positivo.")

    plot_sentiment_hist(sentiment)