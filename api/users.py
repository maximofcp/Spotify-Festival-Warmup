import json

import requests

from api.base import AuthAPI
from models import User


class UserAPI(AuthAPI):
    def me(self) -> User:
        response = requests.get(f'{self.url}me', headers=self.headers())
        parsed_response = json.loads(response.content)

        return User(**parsed_response)
