from src.models.player import Player


def test_add():
    assert 1 + 1 == 2


def test_roll():
    player = Player(name="Chris")
    assert player.cash == 1500
