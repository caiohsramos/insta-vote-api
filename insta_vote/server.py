from flask import Flask, jsonify, request
from flask_cors import CORS
import insta_vote.database as db
import insta_vote.instagram as insta

app = Flask("insta_vote")
CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    status, response = db.ping()
    if status:
        return jsonify({"status": "health", "message": "Mongo is ok"})
    return jsonify({"status": "unhealth", "message": response})


@app.route("/new_post", methods=["POST"])
def new_post():
    payload = request.json
    url = payload["url"]

    try:
        media_id, author = insta.get_info(url)
    except:
        return app.response_class(status=404)
    try:
        db.new_post(url, media_id, author)
    except:
        return app.response_class(status=400)

    return app.response_class(status=201)


@app.route("/battle", methods=["GET"])
def battle():
    posts = db.get_random(2)

    return jsonify(posts)


@app.route("/feed", methods=["GET"])
def feed():
    feed_posts = db.get_most_votes(50)

    return jsonify(feed_posts)


@app.route("/compute", methods=["POST"])
def compute():
    payload = request.json
    try:
        db.compute_battle(payload["winner"], payload["looser"])
    except:
        app.response_class(status=400)

    return app.response_class(status=201)


if __name__ == "__main__":
    app.run("0.0.0.0", 3001)
