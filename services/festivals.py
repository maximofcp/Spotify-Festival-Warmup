from models import Festival
from repositories.festivals import FestivalRepository


class FestivalService:
    def __init__(self, festival_repo: FestivalRepository):
        self.festival_repo = festival_repo

    def read_all(self) -> list[Festival]:
        return self.festival_repo.read_all_active()
