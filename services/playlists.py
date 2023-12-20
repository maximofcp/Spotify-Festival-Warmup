import logging

from api.playlists import PlaylistAPI
from api.searches import SearchAPI
from models import Festival, Playlist, Track, User, Artist
from repositories.playlists import PlaylistRepository


class PlaylistService:
    def __init__(self, search_api: SearchAPI, playlist_api: PlaylistAPI, playlist_repo: PlaylistRepository,
                 tracks_per_artist: int):
        self.search_api = search_api
        self.playlist_api = playlist_api
        self.playlist_repo = playlist_repo
        self.tracks_per_artist = tracks_per_artist

    def create_or_update_playlists_for_festivals(self, festivals: list[Festival], user: User) -> None:
        for festival in festivals:
            playlist, created = self.create_or_update_playlist(festival, user)
            logging.info(f'{"Created" if created else "Updated"} playlist {playlist}!')

    def create_or_update_playlist(self, festival: Festival, user: User) -> tuple[Playlist, bool]:
        name = self._create_playlist_name(festival)
        playlist = self.playlist_repo.get_by_name(name)
        if not playlist:
            return self.create_playlist(name, festival, user), True

        return self.update_playlist(playlist, festival), False

    def update_playlist(self, playlist: Playlist, festival: Festival) -> Playlist:
        remaining_artists_to_add = list(
            filter(lambda a: a.name not in {t.artist.name for t in playlist.tracks}, festival.artists))

        tracks: list[Track] = self._find_spotify_tracks_for_artists(remaining_artists_to_add)
        playlist_track_ids = [t.id for t in playlist.tracks]
        remaining_tracks_to_add = list(filter(lambda t: t.id not in playlist_track_ids, tracks))

        if not remaining_tracks_to_add:
            logging.info(f'No new tracks to add on {playlist}!')
            return playlist

        playlist.add_tracks(remaining_tracks_to_add)

        return self._save(playlist)

    def create_playlist(self, name: str, festival: Festival, user: User) -> Playlist:
        tracks = self._find_spotify_tracks_for_artists(festival.artists)

        playlist = Playlist(name=name, description=self._create_playlist_description(festival, tracks), user=user,
                            tracks=tracks)

        return self._save(playlist)

    def _find_spotify_tracks_for_artists(self, artists: list[Artist]) -> list[Track]:
        tracks: list[Track] = []

        for artist in artists:
            unordered_tracks = self.search_api.tracks_by_artist(artist, self.tracks_per_artist)
            tracks.extend(self._select_top_tracks(unordered_tracks))

        return tracks

    def _save(self, playlist: Playlist) -> Playlist:
        playlist = self.playlist_api.save(playlist)
        self.playlist_repo.upsert(playlist)

        return playlist

    @staticmethod
    def _select_top_tracks(tracks: list[Track]) -> list[Track]:
        return list(sorted(tracks, key=lambda t: t.popularity, reverse=True))

    @staticmethod
    def _create_playlist_name(festival: Festival) -> str:
        return f'{festival.name} [FWU]'

    @staticmethod
    def _create_playlist_description(festival: Festival, tracks: list[Track]) -> str:
        artists = list({t.artist.name for t in tracks})
        description = (f'Auto-generated playlist based on the festival {festival.name}!'
                       f' Featuring artists: {", ".join(artists)}')

        return f'{description[:297]}...'  # description size limit
