from flask import Flask, request, jsonify
import requests

from config import TOKEN

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def create_short_url():
    # Get the url from the request body
    url = request.json.get("url")
    # Get the alias from the request body
    alias = request.json.get("alias")

    # Create the short url
    short_url = create_short_url(url, alias)

    # Return the short url
    return jsonify({"short_url": short_url})


def create_short_url(url, alias):
    # Set the base url
    BASE_URL = "https://api.tinyurl.com"
    # Set the header
    header = {'Authorization': 'Bearer ' + TOKEN}
    # Set the body
    body = {
        "url": url,
        "domain": "tiny.one",
        "alias": alias,
    }
    # Make the request
    response = requests.post(BASE_URL+'/create', data=body, headers=header)
    # Return the short url
    json = response.json()
    return json["data"]["tiny_url"]
