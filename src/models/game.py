import itertools
import random
from typing import List

import click
from pydantic import BaseModel

from models.cards import Card, CardTypes
from models.constants import GameSpaceTypes, PropertyStatus
from models.gamespace import GameSpace
from models.player import Player


class Game(BaseModel):
    spaces: List[GameSpace] = []
    players: List[Player] = []
    chance_cards: List[Card] = []
    cc_cards: List[Card] = []
    jail_index: int = 0

    def add_space(self, space: GameSpace):
        self.spaces.append(space)
        if space.type == GameSpaceTypes.JAIL:
            self.jail_index = len(self.spaces) - 1

    def add_player(self, player: Player):
        self.players.append(player)

    def add_card(self, title, type):
        if type == CardTypes.CHANCE:
            self.chance_cards.append(Card(title=title, type=type))
        else:
            self.cc_cards.append(Card(title=title, type=type))

    def shuffle_cards(self):
        random.shuffle(self.cc_cards)
        random.shuffle(self.chance_cards)
        click.echo("cards shuffled")
        return self

    def send_player_to_just_visiting(self, player: Player):
        player.in_jail = False
        player.jail_count = 0

    def send_player_to_jail(self, player: Player):
        player.position = self.jail_index
        player.in_jail = True
        player.jail_count = 3

    def post_move_action(self, new_space: GameSpace, player: Player):
        if new_space.type == GameSpaceTypes.GO_TO_JAIL:
            click.echo("Going to jail...")
            player.position = self.jail_index
        # TODO: implement drawing of card
        if new_space.type in [GameSpaceTypes.DRAW_CHANCE, GameSpaceTypes.DRAW_CHEST]:
            click.echo("Draw a card")
            return
        # TODO: what if the player doesn't have enough cash?
        if new_space.type == GameSpaceTypes.TAX:
            if player.cash >= new_space.value:
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
        ):
            if click.confirm(f"Property is vacant. Purchase for ${new_space.value}?"):
                if player.cash >= new_space.value:
                    new_space.owner = player
                    new_space.status = PropertyStatus.OWNED
                    player.cash -= new_space.value
                else:
                    click.echo("Sorry, not enough cash.")

    def play(self):
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
        if roll_result < 13:
            click.echo(f"rolled: {roll_result}")
            # if player passes or lands on GO, add 200 to their cash
            if player.position + roll_result >= len(self.spaces):
                player.cash += 200
                click.echo("passed go, added $200")
            player.position = (player.position + roll_result) % len(self.spaces)
            new_space = self.spaces[player.position]
            click.echo(f"player: {player.name} landed on {new_space}")
            self.post_move_action(new_space, player)
            return
        # roll result == 98 when 3 consecutive doubles, go to jail
        if roll_result == 98:
            click.echo("3rd consecutive double, go to jail, fool!")
            self.send_player_to_jail(player)
            return
        if roll_result == 99:
            click.echo("Rolled a double while in jail, now just visiting.")
            self.send_player_to_just_visiting(player)
            return
        else:
            raise Exception(
                f"Uncaught scenarion....roll result: {roll_result} for player: {player}"
            )
