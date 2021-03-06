import re 
import tweepy 
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # Replace the keys and tokens from the Twitter Dev Console 
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 

        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 

            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 

                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    v_query = raw_input("Please enter a keyword to evaluate:\n")
    print("Please wait while we evaluate %s"%v_query )
    tweets = api.get_tweets(query = v_query, count = 200) 
    print("Fetched Tweets: {}".format(len(tweets))) 
    # picking positive tweets from tweets 
    positivetweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # picking negative tweets from tweets 
    negativetweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']    
    print("Positive Tweets: {}".format(len(positivetweets)))
    print("Negative Tweets: {}".format(len(negativetweets)))
    print("Neutral Tweets: {}".format(len(tweets) - len(negativetweets) - len(positivetweets)))
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(positivetweets)/len(tweets))) 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(negativetweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) -(len( negativetweets )+len( positivetweets)))/len(tweets))) 

    #Graph
    objects = ('Positive', 'Neutral', 'Negative')
    y_pos = np.arange(len(objects))
    performance = [len(positivetweets),len(tweets) - len(negativetweets) - len(positivetweets),len(negativetweets)]
    
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Perccentage')
    plt.title('%s Sentiment Analysis'%v_query)    
    plt.show()
    # printing first 5 positive tweets 
    print("\n\nSelected Positive tweets:") 
    print("\n-----------------------------") 
    for tweet in positivetweets[:10]: 
        print(tweet['text'].encode('utf-8')) 

    # printing first 5 negative tweets 
    print("\n\nSelected Negative tweets:") 
    print("\n-----------------------------")
    for tweet in negativetweets[:10]: 
        print(tweet['text'].encode('utf-8')) 

if __name__ == "__main__": 
    # calling main function 
    main()