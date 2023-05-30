import pytest

from src.main import setup_game
from src.models.constants import GameSpaceTypes
from src.models.game import Game
from src.models.gamespace import GameSpace


@pytest.fixture()
def mock_game():
    return Game()


@pytest.fixture()
def mock_full_game() -> Game:
    return setup_game()


@pytest.fixture()
def mock_draining_game() -> Game:
    game = setup_game()
    game.spaces = [
        GameSpace(
            name="Water Works",
            value=150,
            group=None,
            type=GameSpaceTypes.TAX,
        )
        for g in game.spaces
    ]
    for player in game.players:
        player.cash = 75
    return game
