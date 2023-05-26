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
