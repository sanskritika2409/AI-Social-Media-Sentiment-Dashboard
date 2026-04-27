import tweepy
import pandas as pd

bearer_token = "YOUR_TOKEN"

client = tweepy.Client(bearer_token=bearer_token)

query = "zomato OR swiggy lang:en -is:retweet"

tweets = client.search_recent_tweets(
    query=query,
    max_results=50
)

data = []

for tweet in tweets.data:
    data.append([tweet.text])

df = pd.DataFrame(data, columns=["text"])
df.to_csv("data/tweets.csv", index=False)

print("Tweets Saved")