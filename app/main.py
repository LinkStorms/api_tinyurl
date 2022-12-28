from flask import Flask, request, json
from werkzeug.exceptions import HTTPException
from flasgger import Swagger, swag_from

import requests


app = Flask(__name__)
swagger = Swagger(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/create", methods=["POST"])
@swag_from("flasgger_docs/create_short_url.yml")
def create_short_url():
    # Get the url from the request body
    url = request.json.get("url")
    # Get the alias from the request body
    alias = request.json.get("alias")
    # Get the token from the request body
    token = request.json.get("token")

    # Create the short url
    status_code, short_url, errors, code = create_short_url(url, alias, token)

    # Return the short url
    if status_code == 200:
        return {"data": {"short_url": short_url}, "errors": errors, "code": status_code}, status_code
    return {"data": {}, "errors": errors, "code": status_code}, status_code


def create_short_url(url, alias, token):
    # Set the base url
    BASE_URL = "https://api.tinyurl.com"
    # Set the header
    header = {'Authorization': 'Bearer ' + token}
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
    status_code = response.status_code
    if status_code == 200:
        return status_code, json["data"]["tiny_url"], json.get("errors", None), json.get("code")
    return status_code, None, json.get("errors", None), json.get("code")
