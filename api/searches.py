import json

import requests

from api.base import AuthAPI
from models import Artist, Track


class SearchAPI(AuthAPI):
    @property
    def url(self) -> str:
        return f'{super().url}search'

    def tracks_by_artist(self, artist: Artist, limit: int = 20) -> list[Track]:
        response = requests.get(f'{self.url}?q=artist:{artist.name}&type=track&limit={limit}', headers=self.headers())
        parsed_response = json.loads(response.content)

        return [Track(**{**track, 'artist': artist}) for track in parsed_response['tracks']['items']]
