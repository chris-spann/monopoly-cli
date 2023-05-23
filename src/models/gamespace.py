import click
from pydantic import BaseModel

from models.constants import GameSpaceTypes, PropertyStatus
from models.player import Player


class GameSpace(BaseModel):
    name: str
    value: int
    group: str | None
    owner: Player | None = None
    status: str = PropertyStatus.VACANT
    type: str

    def action(self, player: Player, jail_index: int):
        if self.type == GameSpaceTypes.GO_TO_JAIL:
            click.echo("Going to jail...")
            player.position = jail_index
        # TODO: implement drawing of card
        if self.type in [GameSpaceTypes.DRAW_CHANCE, GameSpaceTypes.DRAW_CHEST]:
            click.echo("Draw a card")
            return
        # TODO: what if the player doesn't have enough cash?
        if self.type == GameSpaceTypes.TAX:
            if player.cash >= self.value:
                click.echo(f"Taxed! Paid: {self.value}")
                player.cash -= self.value
        if (
            self.type in [GameSpaceTypes.PROPERTY, GameSpaceTypes.RAILROAD]
            and self.status == PropertyStatus.VACANT
        ):
            if click.confirm(f"Property is vacant. Purchase for ${self.value}?"):
                if player.cash >= self.value:
                    self.owner = player
                    self.status = PropertyStatus.OWNED
                    player.cash -= self.value
                else:
                    click.echo("Sorry, not enough cash.")

    def __repr__(self):
        return (
            f"name: {self.name}, type: {self.type}, group: {self.group}, "
            f"status: {self.status}, price: {self.value}"
        )
