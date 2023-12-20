import logging
import os

from api.auths import Auth
from api.playlists import PlaylistAPI
from api.searches import SearchAPI
from api.users import UserAPI
from models import Festival, Artist, User
from repositories.festivals import FestivalRepository
from repositories.playlists import PlaylistRepository
from services.festivals import FestivalService
from services.playlists import PlaylistService
from utils import read_file


class FestivalFactory:
    @staticmethod
    def create(name: str, artists: list[str]) -> Festival:
        return Festival(name=name, artists=[Artist(name=name) for name in artists])

    @staticmethod
    def read_from_file() -> list[Festival]:
        festivals_raw = read_file()
        festivals: list[Festival] = []

        for festival in festivals_raw:
            name, rest = festival.split(':')
            if name.startswith('!'):
                logging.info(f'Skipping importing festival {name}...')
                continue

            artist_names = [a.strip() for a in rest.split(',')]
            festivals.append(FestivalFactory.create(name.strip(), artist_names))

        return festivals


class AuthFactory:
    @staticmethod
    def create_from_env() -> Auth:
        return Auth(code=os.environ.get("CODE"), client_id=os.environ.get("CLIENT_ID"),
                    client_secret=os.environ.get("CLIENT_SECRET"), redirect_uri=os.environ.get("REDIRECT_URI"))


class ServiceFactory:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.search_api = SearchAPI(auth=auth)
        self.playlist_api = PlaylistAPI(auth=auth)
        self.playlist_repo = RepositoryFactory.playlist()
        self.festival_repo = RepositoryFactory.festival()

    def playlists(self) -> PlaylistService:
        tracks_per_artist = os.environ.get("TRACKS_PER_ARTIST", 20)

        return PlaylistService(search_api=self.search_api, playlist_api=self.playlist_api,
                               playlist_repo=self.playlist_repo, tracks_per_artist=tracks_per_artist)

    def festivals(self) -> FestivalService:
        return FestivalService(festival_repo=self.festival_repo)


class UserFactory:
    def __init__(self, auth: Auth):
        self.user_api = UserAPI(auth=auth)

    def me(self) -> User:
        return self.user_api.me()


class RepositoryFactory:
    @staticmethod
    def festival() -> FestivalRepository:
        return FestivalRepository('festivals')

    @staticmethod
    def playlist() -> PlaylistRepository:
        return PlaylistRepository('playlists')
