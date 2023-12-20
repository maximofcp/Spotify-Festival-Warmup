import logging

from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class Model(BaseModel):
    model_config = ConfigDict(
        extra='ignore',
    )


class User(Model):
    id: str
    name: str = Field(validation_alias=AliasChoices('name', 'display_name'))

    def __str__(self) -> str:
        return f'{self.name}'


class Artist(Model):
    name: str

    def __str__(self) -> str:
        return self.name


class Track(Model):
    id: str
    uri: str
    name: str
    popularity: int
    artist: Artist

    def __str__(self) -> str:
        return f'{self.artist} - {self.name}'


class Playlist(Model):
    id: str = Field(default=None)
    name: str
    description: str = Field(default='')
    tracks: list[Track] = Field(default=[])
    user: User = Field(default=None)
    new_tracks: list[Track] = Field(default=[], exclude=True)

    @property
    def all_tracks(self) -> list[Track]:
        return self.tracks + self.new_tracks

    def add_tracks(self, tracks: list[Track]) -> None:
        logging.info(f'Adding new tracks to playlist {self}: {", ".join([str(t) for t in tracks])}')
        self.new_tracks.extend(tracks)

    def __str__(self) -> str:
        return f'{self.name}'


class Festival(Model):
    name: str
    description: str = Field(default='')
    artists: list[Artist] = Field(default=[])

    def __str__(self) -> str:
        return f'{self.name}: {", ".join(*self.artists)}'
