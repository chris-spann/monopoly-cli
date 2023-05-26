from unittest.mock import patch

from src.models.card import CardTypes
from src.models.constants import GameSpaceTypes, PropertyGroup
from src.models.game import Game
from src.models.gamespace import GameSpace
from src.models.player import Player


def test_add_space():
    game = Game()
    game.add_space(
        GameSpace(
            name="Mediterranean Ave",
            value=60,
            group=PropertyGroup.VIOLET,
            type=GameSpaceTypes.PROPERTY,
        )
    )
    game.add_space(GameSpace(name="Jail", value=200, group=None, type=GameSpaceTypes.JAIL))
    assert len(game.spaces) == 2
    assert game.jail_index == 1


def test_add_player():
    game = Game()
    game.add_player(Player(name="Chris"))
    assert len(game.players) == 1


def test_send_player_to_jail():
    game = Game(jail_index=14)
    player = Player(name="Chris")
    game.add_player(player)
    game.send_player_to_jail(player)
    assert player.position == 14
    assert player.in_jail
    assert player.jail_count == 3


def test_send_player_to_just_visiting():
    game = Game(jail_index=14)
    player = Player(name="Chris")
    game.add_player(player)
    game.send_player_to_just_visiting(player)
    assert player.position == 14
    assert not player.in_jail
    assert player.jail_count == 0


def test_add_card():
    game = Game()
    game.add_card("Card1", CardTypes.CHANCE)
    assert len(game.chance_cards) == 1
    assert len(game.cc_cards) == 0
    game.add_card("Card2", CardTypes.COMMUNITY_CHEST)
    assert len(game.cc_cards) == 1


def test_shuffle_cards():
    game = Game()
    game.add_card("Card1", CardTypes.CHANCE)
    game.add_card("Card2", CardTypes.CHANCE)
    game.add_card("Card3", CardTypes.CHANCE)
    game.add_card("Card4", CardTypes.CHANCE)
    game.add_card("Card5", CardTypes.CHANCE)
    game.add_card("Card6", CardTypes.CHANCE)
    game.add_card("Card7", CardTypes.CHANCE)
    game.add_card("Card8", CardTypes.CHANCE)
    game.add_card("Card9", CardTypes.CHANCE)
    game.add_card("Card10", CardTypes.CHANCE)
    game.add_card("Card11", CardTypes.CHANCE)
    orig = game.chance_cards.copy()
    game.shuffle_cards()
    assert len(game.chance_cards) == len(orig)
    assert game.chance_cards != orig


def test_draw_card():
    game = Game()
    game.add_card("Card1", CardTypes.CHANCE)
    game.add_card("Card2", CardTypes.COMMUNITY_CHEST)
    draw_1 = game.draw_card(CardTypes.CHANCE)
    draw_2 = game.draw_card(CardTypes.COMMUNITY_CHEST)
    assert draw_1.title == "Card1"
    assert draw_2.title == "Card2"


def test_post_move_go_to_jail():
    game = Game()
    game.add_player(Player(name="Chris"))
    go_to_jail_space = GameSpace(
        name="Go to Jail", value=200, group=None, type=GameSpaceTypes.GO_TO_JAIL
    )
    player = game.players[0]
    game.post_move_action(go_to_jail_space, player)
    assert player.in_jail


@patch("src.models.game.Game.draw_card", return_value=None)
def test_post_move_draw_card(mock_draw_card):
    game = Game()
    player = Player(name="Chris")
    game.add_player(player)
    chance_card_space = GameSpace(
        name="Chance Card", value=200, group=None, type=GameSpaceTypes.DRAW_CHANCE
    )
    player = game.players[0]
    game.post_move_action(chance_card_space, player)
    assert mock_draw_card.called_once()


def test_post_move_tax():
    game = Game()
    player = Player(name="Chris")
    game.add_player(player)
    game.post_move_action(
        GameSpace(
            name="Electric Company",
            value=150,
            group=None,
            type=GameSpaceTypes.TAX,
        ),
        player,
    )
    assert player.cash == 1350
