import os
import json
from pymongo import MongoClient
from bson import json_util

DB = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/main")).insta_vote


def ping():
    try:
        DB.command("ping")
        return True, None
    except Exception as e:
        return False, str(e)


def new_post(url, media_id, author):
    DB.posts.insert_one(
        {"url": url, "author": author, "media_id": media_id, "wins": 0, "losses": 0}
    )


def get_random(n):
    posts = DB.posts.aggregate([{"$sample": {"size": n}}])
    return [json.loads(json.dumps(post, default=json_util.default)) for post in posts]


def get_most_votes(n):
    top_posts = DB.posts.find().sort([("wins", -1), ("losses", 1)]).limit(n)

    return [
        json.loads(json.dumps(post, default=json_util.default)) for post in top_posts
    ]


def compute_battle(winner, looser):
    DB.posts.update({"media_id": winner}, {"$inc": {"wins": 1}})
    DB.posts.update({"media_id": looser}, {"$inc": {"losses": 1}})
