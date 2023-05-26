from src.models.gamespace import GameSpace


def test_gamespace():
    space = GameSpace(
        name="Connecticut Ave",
        value=120,
        group="light-blue",
        type="property",
    )
    rep = space.__repr__()

    assert space.value == 120
    assert rep == (
        f"name: {space.name}, type: {space.type}, group: {space.group}, "
        f"status: {space.status}, price: {space.value}"
    )
