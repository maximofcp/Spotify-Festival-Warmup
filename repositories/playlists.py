from typing import Optional

from tinydb import Query

from models import Playlist
from repositories.base import BaseRepository


class PlaylistRepository(BaseRepository):
    def list_all(self) -> list[Playlist]:
        return [Playlist(**p) for p in self.table.all()]

    def get_by_name(self, name: str) -> Optional[Playlist]:
        query = Query()
        data = self.table.search(query.name == name)

        return Playlist(**data[0]) if data else None

    def upsert(self, playlist: Playlist) -> None:
        data = playlist.model_dump()
        if playlist.new_tracks:
            data['tracks'] = [t.model_dump() for t in playlist.all_tracks]

        self.table.upsert(data, Query().id == playlist.id)
