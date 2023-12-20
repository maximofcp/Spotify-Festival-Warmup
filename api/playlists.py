import json

import requests

from api.base import AuthAPI
from models import Playlist, Track
from utils import chunks


class PlaylistAPI(AuthAPI):
    uri_limit = 100  # stated in documentation

    def headers(self) -> dict:
        return {**super().headers(), 'Content-Type': 'application/json'}

    def save(self, playlist: Playlist) -> Playlist:
        if not playlist.id:
            data = {'name': playlist.name, 'description': playlist.description, 'public': False}
            url = f'{super().url}users/{playlist.user.id}/playlists'
            response = requests.post(url, data=json.dumps(data), headers=self.headers())
            parsed_response = json.loads(response.content)

            playlist.id = parsed_response['id']

            self.add_tracks(playlist.id, playlist.tracks)

            return playlist

        self.add_tracks(playlist.id, playlist.new_tracks)

        return playlist

    def add_tracks(self, playlist_id: str, tracks: list[Track]) -> None:
        uri_chunks = chunks(tracks, self.uri_limit)

        for chunk in uri_chunks:
            data = {'uris': [c.uri for c in chunk], 'position': 0}
            url = f'{super().url}playlists/{playlist_id}/tracks'

            # TODO: lookup for success response
            requests.post(url, data=json.dumps(data), headers=self.headers())
