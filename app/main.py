from flask import Flask, request, json
from werkzeug.exceptions import HTTPException
from flasgger import Swagger

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
      - name: token
        type: string
        in: body
        example: "KfX1xzgntbZtRsyHb9eNgl8b4oJiLHCIdZlKymi5nRBk33R8UGSOVElZZGUT"
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
                properties:
                    code:
                        type: integer
                        description: The status code
                        example: 200
                    data:
                        type: object
                        properties:
                            short_url:
                                type: string
                                description: The short url
                                example: "https://tiny.one/flask2"
                    errors:
                        type: array
                        items:
                            type: string
                        description: The errors
                        example: []
        401:
            description: Not authorized to use to access this API endpoint or resource. Please check your API token
            schema:
                properties:
                    code:
                        type: integer
                        description: The status code
                        example: 401
                    data:
                        type: object
                        example: {}
                    errors:
                        type: array
                        items:
                            type: string
                        description: The errors
                        example: ["Unauthorized"]
        405:
            description: You do not have permission to access this resource
            schema:
                properties:
                    code:
                        type: integer
                        description: The status code
                        example: 405
                    data:
                        type: object
                        example: {}
                    errors:
                        type: array
                        items:
                            type: string
                        description: The errors
                        example: ["Method Not Allowed"]
        422:
            description: Validation failed on one of the properties, please check the errors in the response body.
            schema:
                properties:
                    code:
                        type: integer
                        description: The status code
                        example: 422
                    data:
                        type: object
                        example: {}
                    errors:
                        type: array
                        items:
                            type: string
                        description: The errors
                        example: [
                            "Invalid URL",
                            "Alias field is too long"
                        ]
        5XX:
            description: There was an unexpected error processing your request.
            schema:
                properties:
                    code:
                        type: integer
                        description: The status code
                        example: 5XX
                    data:
                        type: object
                        example: {}
                    errors:
                        type: array
                        items:
                            type: string
                        description: The errors
                        example: ["Something went wrong"]
    """
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
