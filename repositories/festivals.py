from tinydb import Query

from models import Festival, Artist
from repositories.base import BaseRepository


class FestivalRepository(BaseRepository):
    def read_all_active(self) -> list[Festival]:
        query = Query()
        data = self.table.search(query.include == True)

        festivals: list[Festival] = []

        for entry in data:
            festival = Festival(name=entry['name'])
            festival.artists = [Artist(name=name) for name in entry['artists']]
            festivals.append(festival)

        return festivals
