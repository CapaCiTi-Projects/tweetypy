"""
MongoDB Output Document Structure

{
    tweeterhandle: @<handle>,
    follwerCount: <int: followCount>,
    followingCount: <int: followingCount>,
    tweets: [
        
    ],
    timestamp: <date>,
    lastUpdateCheck: <date>
}
"""

import datetime
import json
from string import Template

import pymongo
import tweepy

import localsettings


def load_settings():
    settings = {}
    for var in dir(localsettings):
        if var.startswith("__"):
            continue
        settings[var] = getattr(localsettings, var)
    return settings


def get_miners(user, passwd):
    dbname = "tweetypy"

    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{passwd}@cluster0.xjgrr.mongodb.net/{dbname}?retryWrites=true&w=majority")

    db = client[dbname]
    coll = db["miner"]
    coll_agg = coll.aggregate([
        {"$unset": "tweets"}
    ])

    miners = list(coll_agg)

    return miners


def update_many(mongocred: dict, data: list, collname: str, **findquery) -> None:
    user = mongocred["MONGO_USER"]
    passwd = mongocred["MONGO_PASS"]
    dbname = "tweetypy"

    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{passwd}@cluster0.xjgrr.mongodb.net/{dbname}?retryWrites=true&w=majority")

    db = client[dbname]
    coll = db[collname]

    operations = []
    for item in data:
        find = {}
        for key in findquery:
            if type(findquery[key]) is str:
                find[key] = findquery[key].format(item[key])

        operations.append(
            pymongo.ReplaceOne(find, item, upsert=True)
        )

    if len(operations) > 0:
        bulk_res = coll.bulk_write(operations, ordered=False)
        return bulk_res
    return None


def get_api(api_key, secret_key):
    auth = tweepy.AppAuthHandler(api_key, secret_key)

    api = tweepy.API(auth)
    return api


def update(mongocreds, miners, api):
    miner_data = []
    tweet_data = []

    # Loop to generate the miner data and the tweets for storing in Mongo.
    for m in miners:
        handle = m["handle"]
        miner = api.get_user(handle)
        minerd = miner._json

        # Setting base miner data, from the get_user API function.
        miner_updated = {}
        miner_updated["_cls"] = "Miner"
        miner_updated["tid"] = minerd["id_str"]
        miner_updated["name"] = minerd["name"]
        miner_updated["handle"] = minerd["screen_name"]
        miner_updated["is_protected"] = minerd["protected"]
        miner_updated["follower_count"] = minerd["followers_count"]
        miner_updated["following_count"] = minerd["friends_count"]
        miner_updated["is_profile_image_set"] = not minerd["default_profile_image"]
        miner_updated["last_updated"] = datetime.datetime.now()

        # Getting Tweets data for storage in MongoDB.
        miner_tweets = []
        for status in miner.timeline():
            statusd = status._json

            tweet = {}
            tweet["_cls"] = "Status"
            tweet["user"] = {
                "tid": statusd["user"]["id_str"],
                "handle": statusd["user"]["screen_name"]
            }
            tweet["tid"] = statusd["id_str"]
            tweet["creationDate"] = statusd["created_at"]
            tweet["hashtags"] = statusd["entities"]["hashtags"]

            tweet["retweet_count"] = statusd["retweet_count"]
            tweet["favourite_count"] = statusd["favorite_count"]

            miner_tweets.append(tweet)

        miner_data.append(miner_updated)
        tweet_data.extend(miner_tweets)

    update_many(mongocreds, miner_data, "miner", handle="{0}")
    update_many(mongocreds, tweet_data, "status", tid="{0}")


def main():
    settings = load_settings()

    miners = get_miners(settings["MONGO_USER"], settings["MONGO_PASS"])
    api = get_api(settings["TWITTER_API_KEY"], settings["TWITTER_SECRET_KEY"])

    update({
        "MONGO_USER": settings["MONGO_USER"], "MONGO_PASS": settings["MONGO_PASS"]
    }, miners, api)


if __name__ == "__main__":
    main()
