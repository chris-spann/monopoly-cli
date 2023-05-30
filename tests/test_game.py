from unittest.mock import patch

from src.models.card import CardTypes
from src.models.constants import GameSpaceTypes, PropertyGroup, PropertyStatus, RollResultCodes
from src.models.game import Game
from src.models.gamespace import GameSpace
from src.models.player import Player


def test_add_space(mock_game):
    mock_game.add_space(
        GameSpace(
            name="Mediterranean Ave",
            value=60,
            group=PropertyGroup.VIOLET,
            type=GameSpaceTypes.PROPERTY,
        )
    )
    mock_game.add_space(GameSpace(name="Jail", value=200, group=None, type=GameSpaceTypes.JAIL))
    assert len(mock_game.spaces) == 2
    assert mock_game.jail_index == 1


def test_add_player(mock_game):
    mock_game.add_player(Player(name="Chris"))
    assert len(mock_game.players) == 1


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


def test_add_card(mock_game):
    mock_game.add_card("Card1", CardTypes.CHANCE)
    assert len(mock_game.chance_cards) == 1
    assert len(mock_game.cc_cards) == 0
    mock_game.add_card("Card2", CardTypes.COMMUNITY_CHEST)
    assert len(mock_game.cc_cards) == 1


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
    player = Player(name="Chris", cash=1500)
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


def test_post_move_owned_property(capsys):
    game = Game()
    player_1 = Player(name="Chris")
    player_2 = Player(name="Benny")
    game.add_player(player_1)
    game.add_player(player_2)
    game.post_move_action(
        GameSpace(
            name="Oriental Ave",
            value=100,
            group=PropertyGroup.LIGHT_BLUE,
            type=GameSpaceTypes.PROPERTY,
            owner=player_2,
            status=PropertyStatus.OWNED,
        ),
        player_1,
    )
    captured = capsys.readouterr()
    assert "property is owned by" in captured.out


@patch("src.models.game.click.confirm", return_value=True)
def test_post_move_property_purchase_success(mock_confirm):
    game = Game()
    player_1 = Player(name="Chris", cash=200)
    property = GameSpace(
        name="Oriental Ave",
        value=100,
        group=PropertyGroup.LIGHT_BLUE,
        type=GameSpaceTypes.PROPERTY,
    )
    game.add_player(player_1)
    game.post_move_action(property, player_1)
    assert player_1.cash == 100
    assert property.status == PropertyStatus.OWNED
    assert property.owner == player_1


@patch("src.models.game.click.confirm", return_value=True)
def test_post_move_property_purchase_fail(mock_confirm, capsys):
    game = Game()
    player = Player(name="Chris", cash=75)
    game.add_player(player)
    property = GameSpace(
        name="Oriental Ave",
        value=100,
        group=PropertyGroup.LIGHT_BLUE,
        type=GameSpaceTypes.PROPERTY,
    )

    game.post_move_action(property, player)
    captured = capsys.readouterr()
    assert "Sorry, not enough cash." in captured.out
    assert property.status == PropertyStatus.VACANT
    assert property.owner is None
    assert player.cash == 75


@patch("src.models.game.Player.roll", return_value=4)
@patch("src.models.game.click.confirm", return_value=False)
def test_player_turn(mock_confirm, mock_roll, mock_full_game):
    player = mock_full_game.players[0]
    starting_pos = player.position
    mock_full_game.player_turn(player)

    assert player.position == starting_pos + 4


@patch("src.models.game.Player.roll", return_value=11)
@patch("src.models.game.click.confirm", return_value=False)
def test_player_turn_pass_go(mock_confirm, mock_roll, mock_full_game):
    player = mock_full_game.players[0]
    player.position = 34
    mock_full_game.player_turn(player)

    assert player.position == 5
    assert player.cash == 1700


@patch("src.models.game.Player.roll", return_value=RollResultCodes.THIRD_DOUBLE)
def test_player_turn_third_double(mock_roll, mock_full_game, capsys):
    player = mock_full_game.players[0]
    mock_full_game.player_turn(player)
    captured = capsys.readouterr()

    assert player.in_jail
    assert "3rd consecutive double, go to jail, fool!" in captured.out
    assert player.position == mock_full_game.jail_index


@patch("src.models.game.Player.roll", return_value=RollResultCodes.JAIL_DOUBLE)
def test_player_turn_jail_double(mock_roll, mock_full_game):
    player = mock_full_game.players[0]
    player.in_jail = True
    player.jail_count = 3
    mock_full_game.player_turn(player)

    assert player.position == mock_full_game.jail_index
    assert not player.in_jail


@patch("src.models.game.Player.roll", return_value=1)
def test_play_tax(mock_roll, mock_draining_game, capsys):
    mock_draining_game.play()
    assert mock_draining_game.no_cash_players == 2


@patch("src.models.game.Game.post_move_action", return_value=None)
def test_play_no_cash(mock_post_move, mock_full_game, capsys):
    for player in mock_full_game.players:
        player.cash = 0
    print(mock_full_game.players[0].cash)
    mock_full_game.play()
    assert mock_full_game.no_cash_players == len(mock_full_game.players)
    captured = capsys.readouterr()
    assert "game over" in captured.out
