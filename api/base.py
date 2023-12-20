import json
from abc import ABC

from api.auths import Auth


class AuthAPI(ABC):
    BASE_URL: str = "https://api.spotify.com/v1/"

    def __init__(self, auth: Auth):
        self.auth = auth

    @property
    def url(self) -> str:
        return self.BASE_URL

    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.auth.token()}"}

    @classmethod
    def parse_response(cls, response, data_class):
        parsed_response = json.loads(response.content)

        return data_class(**parsed_response)
