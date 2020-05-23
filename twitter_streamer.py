from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

    
class Listener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.counter = 0
        self.limit = 10
        
    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            self.counter += 1
                
        except BaseException as e:
            print("Error on_data %s" % str(e))
        if self.counter < self.limit:
                return True
        else:
            stream.disconnect()
            
        
    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
    hash_tag_list = ["corona virus", "covid19", "pandemic"]
    fetched_tweets_filename = "results.json"
    listener = Listener(fetched_tweets_filename)
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track = hash_tag_list)

    
    
