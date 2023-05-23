import itertools
from typing import List

import click
from pydantic import BaseModel

from models.cards import Card, CardTypes
from models.constants import GameSpaceTypes
from models.gamespace import GameSpace
from models.player import Player


class Game(BaseModel):
    spaces: List[GameSpace] = []
    players: List[Player] = []
    chance_cards: List[Card] = []
    cc_cards: List[Card] = []
    jail_index: int | None

    def add_space(self, space: GameSpace):
        self.spaces.append(space)
        if space.type == GameSpaceTypes.JAIL:
            self.jail_index = len(self.spaces) - 1

    def add_player(self, player: Player):
        self.players.append(player)

    def add_card(self, title, type):
        if type == CardTypes.CHANCE:
            self.chance_cards.append(Card(title, type))
        else:
            self.cc_cards.append(Card(title, type))

    def send_player_to_jail(self, player: Player):
        player.position = self.jail_index
        player.in_jail = True
        player.jail_count = 3

    def play(self):
        click.echo(f"game spaces: {len(self.spaces)}")
        no_cash_players = 0
        list_buff = itertools.cycle(self.players)
        for player in list_buff:
            # skip turn if in jail
            if player.jail_count > 0:
                click.echo("player in jail. skipping turn")
                player.jail_count -= 1
                continue
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
        click.echo(f"rolled: {roll_result}")
        # roll result ==0 when 3 consecutive doubles, go to jail
        if roll_result == 0:
            self.send_player_to_jail(player)
        # if player passes or lands on GO, add 200 to their cash
        if player.position + roll_result >= len(self.spaces):
            player.cash += 200
            click.echo("passed go, added $200")
        player.position = (player.position + roll_result) % len(self.spaces)
        new_space = self.spaces[player.position]
        click.echo(f"player: {player.name} landed on {new_space}")
        new_space.action(player, self.jail_index)
        return
