from insta_vote.server import app

if __name__ == "__main__":
    app.run("0.0.0.0", 3001, debug=True)
