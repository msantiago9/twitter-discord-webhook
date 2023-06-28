from datetime import datetime, timedelta
import os
import dotenv
import time
import pytz
import requests
import snscrape.modules.twitter as sntwitter
import pandas as pd
from tendo import singleton

def fetch_tweets(count: int, twitter_handle: str) -> pd.DataFrame:
    # Created a list to append all tweet attributes(data)
    attributes_container = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(f"from:{twitter_handle}").get_items()
    ):
        if i >= count:
            break
        attributes_container.append(
            [tweet.date, tweet.likeCount, tweet.url, tweet.rawContent]
        )

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(
        attributes_container,
        columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"],
    )

    return tweets_df


def send_to_discord(tweets: pd.DataFrame, current: datetime, webhook_url: str, is_dev: str) -> datetime:

    for i in reversed(tweets.index):
        tweet_time = tweets["Date Created"][i].to_pydatetime()
        print(f"tweet time: {tweet_time}")
        if tweet_time > (current - timedelta(days=365) if is_dev == "true" else current):
            print("Sending Tweet...")
            data = {"content": f"{tweets['Source of Tweet'][i]}"}
            result = requests.post(webhook_url, json=data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Sent to Discord, code {}.".format(result.status_code))
            current = tweet_time + timedelta(seconds=1)
        else:
            print("Tweet already sent, skipping...")
    return current


def main():
    
    me = singleton.SingleInstance()
    # Load the current environment
    dotenv.load_dotenv(dotenv.find_dotenv(filename="config.txt"))
    webhook_url = os.getenv("WEBHOOK_URL")
    twitter_handle = os.getenv("TWITTER_HANDLE")
    is_dev = (os.getenv("IS_DEV") == "true") # true or false. sends duplicates by polling for tweets made in the last 24 hours.
    current = datetime.now(pytz.timezone("UTC"))
    count = 5 if not is_dev else 1

    while True:
        try:
            # Fetch 5 latest tweets every 1800 seconds (30 minutes)
            # Never send duplicates. UNLESS is_dev is set to true.
            tweets = fetch_tweets(count=count, twitter_handle=twitter_handle)
            print(f"current time: {current}")
            current = send_to_discord(tweets=tweets, current=current, webhook_url=webhook_url, is_dev=is_dev)
            if not is_dev:
                time.sleep(1800)
            else:
                break
        except:
            time.sleep(1800)
            continue


if __name__ == "__main__":
    main()
