import os

from flask import Flask, request

from api.auths import Authorize

app = Flask(__name__)


@app.route("/generate-code")
def generate_code():
    return f'Insert this code in the app settings: {request.args.get("code")}'


def authorize():
    Authorize(client_id=os.environ.get("CLIENT_ID"), redirect_uri=os.environ.get("REDIRECT_URI")).open()


authorize()
