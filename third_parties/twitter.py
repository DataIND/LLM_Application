import os 
import tweepy
import requests



twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
)

def scraper_user_tweets(username,num_tweet=5,mock:bool=False):

    """
    Scapes a twitter user's original tweets(i.e not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", "url"
    """

    tweet_list = []
    if mock:
        EDEN_TWITTER_GIST =""
        tweets = requests.get(EDEN_TWITTER_GIST,timeout=5).json()

        for tweet in tweets:

            tweet_dict = {}
            tweet_dict["text"] = tweet["text"]
            tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
            tweet_list.append(tweet_dict)

    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id,max_results=num_tweet,exclude=["retweets","replies"]
        )

        for tweet in tweets.data:
            tweet_dict = {}
            tweet_dict["text"] = tweet["text"]
            tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
            tweet_list.append(tweet_dict)


if __name__ == "__main__":

    tweets = scraper_user_tweets(username="EdenEmarco177")
    print(tweets)