import json
import logging
import os
import webbrowser
from functools import cache

import requests


class Authorize:
    def __init__(self, client_id: str, redirect_uri: str):
        self.redirect_uri = redirect_uri
        self.response_type = 'code'
        self.client_id = client_id
        self.scopes = 'playlist-modify-private playlist-read-private'

    def url(self) -> str:
        return f'https://accounts.spotify.com/authorize?response_type={self.response_type}&client_id={self.client_id}&scope={self.scopes}&redirect_uri={self.redirect_uri}'

    def open(self):
        webbrowser.open(self.url())


class Token:
    def __init__(self, code: str, client_id: str, client_secret: str, redirect_uri: str):
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type: str = "authorization_code"
        self.redirect_uri: str = redirect_uri

    def url(self) -> str:
        return f"https://accounts.spotify.com/api/token?grant_type={self.grant_type}&redirect_uri={self.redirect_uri}&code={self.code}"

    def headers(self) -> dict:
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_access_token(self) -> str:
        if token := os.environ.get("TOKEN"):
            return token

        response = requests.post(self.url(), headers=self.headers(), auth=(self.client_id, self.client_secret))
        parsed_response = json.loads(response.content)

        token = parsed_response['access_token']
        logging.info(token)

        return token


class Auth:
    def __init__(self, code: str, client_id: str, client_secret: str, redirect_uri: str):
        self.token_api = Token(code=code, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    @cache
    def token(self) -> str:
        return self.token_api.get_access_token()
