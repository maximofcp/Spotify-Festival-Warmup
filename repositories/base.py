from tinydb import TinyDB


class BaseRepository:
    def __init__(self, db_name: str):
        self.db = TinyDB(f'repositories/data/{db_name}.json')
        self.table = self.db.table(db_name)
