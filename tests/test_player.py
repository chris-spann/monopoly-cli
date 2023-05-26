from unittest.mock import patch

from src.models.player import Player

mocked_player = Player(name="Bunny", prev_double=[False, True, True])


@patch("src.models.player.Player", return_value=mocked_player)
def test_roll_die(mock_Player):
    player = mock_Player()
    roll_1, roll_2 = player.roll_die()
    assert type(roll_1) == int
    assert type(roll_2) == int
    assert roll_1 + roll_2 < 13


@patch("src.models.player.Player", return_value=mocked_player)
@patch("src.models.player.Player.roll_die", return_value=(3, 3))
def test_third_double_roll_returns_98(mock_roll_die, mock_Player):
    player = mock_Player()
    roll_result = player.roll()
    mock_roll_die.assert_called_once()
    assert roll_result == 98


@patch("src.models.player.Player", return_value=mocked_player)
@patch("src.models.player.Player.roll_die", return_value=(3, 3))
def test_third_double_roll_in_jail_returns_99(mock_roll_die, mock_Player):
    player = mock_Player()
    player.in_jail = True
    roll_result = player.roll()
    mock_roll_die.assert_called_once()
    assert roll_result == 99


@patch("src.models.player.Player", return_value=mocked_player)
@patch("src.models.player.Player.roll_die", return_value=(3, 2))
def test_non_double_roll_returns_sum(mock_roll_die, mock_Player):
    player = mock_Player()
    roll_result = player.roll()
    mock_roll_die.assert_called_once()
    assert roll_result == 5


@patch("src.models.player.Player", return_value=mocked_player)
@patch("src.models.player.Player.roll_die", return_value=(3, 2))
def test_non_double_roll_in_jail_returns_zero(mock_roll_die, mock_Player):
    player = mock_Player()
    player.in_jail = True
    player.jail_count = 2
    roll_result = player.roll()
    mock_roll_die.assert_called_once()
    assert roll_result == 0
    assert player.jail_count == 1
    assert player.in_jail
