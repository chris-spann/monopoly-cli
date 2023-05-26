from enum import StrEnum

from pydantic import BaseModel


class CardTypes(StrEnum):
    COMMUNITY_CHEST = "community_chest"
    CHANCE = "chance"


class Card(BaseModel):
    title: str
    type: str

    def __repr__(self):
        return f"title: {self.title}, type: {self.type}"
