import itertools
import random

import click
from pydantic import BaseModel

from models.card import Card, CardTypes
from models.constants import GameSpaceTypes, PropertyStatus, RollResultCodes
from models.gamespace import GameSpace
from models.player import Player


class Game(BaseModel):
    spaces: list[GameSpace] = []
    players: list[Player] = []
    chance_cards: list[Card] = []
    cc_cards: list[Card] = []
    jail_index: int = 0

    def add_space(self, space: GameSpace) -> None:
        self.spaces.append(space)
        if space.type == GameSpaceTypes.JAIL:
            self.jail_index = len(self.spaces) - 1

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def add_card(self, title, type) -> None:
        if type == CardTypes.CHANCE:
            self.chance_cards.append(Card(title=title, type=type))
        else:
            self.cc_cards.append(Card(title=title, type=type))

    def shuffle_cards(self):
        random.shuffle(self.cc_cards)
        random.shuffle(self.chance_cards)
        click.echo("cards shuffled")
        return self

    def draw_card(self, type: str) -> Card:
        if type == CardTypes.CHANCE:
            return self.chance_cards[0]
        return self.cc_cards[0]

    def send_player_to_just_visiting(self, player: Player) -> None:
        player.in_jail = False
        player.jail_count = 0
        player.position = self.jail_index

    def send_player_to_jail(self, player: Player) -> None:
        player.in_jail = True
        player.jail_count = 3
        player.position = self.jail_index

    def post_move_action(self, new_space: GameSpace, player: Player) -> None:
        if new_space.type == GameSpaceTypes.GO_TO_JAIL:
            click.echo("Going to jail...")
            self.send_player_to_jail(player)
        # TODO: implement drawing of card
        if new_space.type in [GameSpaceTypes.DRAW_CHANCE, GameSpaceTypes.DRAW_CHEST]:
            click.echo("Draw a card")
            self.draw_card(new_space.type)
        # TODO: what if the player doesn't have enough cash?
        if new_space.type == GameSpaceTypes.TAX and player.cash >= new_space.value:
            click.echo(f"Taxed! Paid: {new_space.value}")
            player.cash -= new_space.value
        # TODO: if new space type is TAX_INCOME, present the choice of 10% of cash or $200
        # TODO: if property is owned, determine the rent amount and pay it
        if (
            new_space.type in [GameSpaceTypes.PROPERTY, GameSpaceTypes.RAILROAD]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner != player
        ):
            click.echo(f"property is owned by {new_space.owner}. Please pay 1 million dollars.")
        if (
            new_space.type in [GameSpaceTypes.PROPERTY, GameSpaceTypes.RAILROAD]
            and new_space.status == PropertyStatus.VACANT
        ) and click.confirm(f"Property is vacant. Purchase for ${new_space.value}?"):
            if player.cash >= new_space.value:
                new_space.owner = player
                new_space.status = PropertyStatus.OWNED
                player.cash -= new_space.value
            else:
                click.echo("Sorry, not enough cash.")

    def play(self) -> None:
        click.echo(f"game spaces: {len(self.spaces)}")
        no_cash_players = 0
        list_buff = itertools.cycle(self.players)
        for player in list_buff:
            self.player_turn(player)
            click.echo("----------")
            if player.cash == 0:
                no_cash_players += 1
                click.echo(f"player: {player.name} is out of cash")
                continue
            if no_cash_players == len(self.players):
                click.echo("game over, no players with cash")
                break

    def player_turn(self, player: Player) -> None:
        click.echo(f"player: {player.name}'s turn")
        starting_space = self.spaces[player.position]
        click.echo(f"player: {player.name} started on {starting_space}")
        roll_result = player.roll()
        # roll result == 98 when 3 consecutive doubles, go to jail
        if roll_result == RollResultCodes.THIRD_DOUBLE:
            click.echo("3rd consecutive double, go to jail, fool!")
            self.send_player_to_jail(player)
            return
        if roll_result == RollResultCodes.JAIL_DOUBLE:
            click.echo("Rolled a double while in jail, now just visiting.")
            self.send_player_to_just_visiting(player)
            return
        click.echo(f"rolled: {roll_result}")
        # if player passes or lands on GO, add 200 to their cash
        if player.position + roll_result >= len(self.spaces):
            player.cash += 200
            click.echo("passed go, added $200")
        player.position = (player.position + roll_result) % len(self.spaces)
        new_space = self.spaces[player.position]
        click.echo(f"player: {player.name} landed on {new_space}")
        self.post_move_action(new_space, player)
