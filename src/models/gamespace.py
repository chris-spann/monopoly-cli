from pydantic import BaseModel

from models.constants import PropertyStatus
from models.player import Player


class GameSpace(BaseModel):
    name: str
    value: int
    group: str | None
    owner: Player | None = None
    status: str = PropertyStatus.VACANT
    type: str

    def __repr__(self) -> str:
        return (
            f"name: {self.name}, type: {self.type}, group: {self.group}, "
            f"status: {self.status}, price: {self.value}"
        )
