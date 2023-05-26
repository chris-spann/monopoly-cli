from src.models.card import Card, CardTypes


def test_card():
    chance = Card(title="Some title", type=CardTypes.CHANCE)
    assert chance.__repr__() == "title: Some title, type: chance"
