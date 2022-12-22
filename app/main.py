from flask import Flask, request, jsonify
from flasgger import Swagger
import requests

from config import TOKEN


app = Flask(__name__)
swagger = Swagger(app)


@app.route("/create", methods=["POST"])
def create_short_url():
    """ Creating a short url with alias if provided, otherwise a random alias
    will be generated
    ---
    parameters:
      - name: url
        type: string
        in: body
        example: "https://flask.palletsprojects.com/en/2.2.x/"
        required: true
      - name: alias
        type: string
        in: body
        example: "flask2"
        required: false
    responses:
      200:
        description: Created short url will be returned
        schema:
            id: short_url
            properties:
                short_url:
                    type: string
                    description: The short url
                    example: "https://tiny.one/flask2"
    """
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
