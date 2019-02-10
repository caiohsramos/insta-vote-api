import json
import requests

INSTAGRAM_API = "https://api.instagram.com/"


def get_info(url):
    params = dict(url=url)
    r = requests.get(INSTAGRAM_API + "oembed", params=params)
    if r.status_code == 404:
        raise Exception
    data = json.loads(r.text)
    return data["media_id"], data["author_name"]
