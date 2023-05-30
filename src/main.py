from models.card import Card, CardTypes
from models.constants import GameSpaceTypes, PropertyGroup
from models.game import Game
from models.gamespace import GameSpace
from models.player import Player


def setup_game() -> Game:
    game = Game()
    default_spaces = [
        GameSpace(name="GO", value=200, group=None, type=GameSpaceTypes.FREE),
        GameSpace(
            name="Mediterranean Ave",
            value=60,
            group=PropertyGroup.VIOLET,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Community Chest",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHEST,
        ),
        GameSpace(
            name="Baltic Ave",
            value=60,
            group=PropertyGroup.VIOLET,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Income Tax",
            value=200,
            group=None,
            type=GameSpaceTypes.TAX_INCOME,
        ),
        GameSpace(
            name="Reading Railroad",
            value=200,
            group=PropertyGroup.RAILROAD,
            type=GameSpaceTypes.RAILROAD,
        ),
        GameSpace(
            name="Oriental Ave",
            value=100,
            group=PropertyGroup.LIGHT_BLUE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Chance",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHANCE,
        ),
        GameSpace(
            name="Vermont Ave",
            value=100,
            group=PropertyGroup.LIGHT_BLUE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Connecticut Ave",
            value=120,
            group=PropertyGroup.LIGHT_BLUE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Jail",
            value=500,
            group=None,
            type=GameSpaceTypes.JAIL,
        ),
        GameSpace(
            name="St Charles Place Ave",
            value=140,
            group=PropertyGroup.PURPLE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Electric Company",
            value=150,
            group=None,
            type=GameSpaceTypes.TAX,
        ),
        GameSpace(
            name="States Ave",
            value=140,
            group=PropertyGroup.PURPLE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Virginia Ave",
            value=160,
            group=PropertyGroup.PURPLE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Pennsylvania Railroad",
            value=200,
            group=PropertyGroup.RAILROAD,
            type=GameSpaceTypes.RAILROAD,
        ),
        GameSpace(
            name="St James Place",
            value=180,
            group=PropertyGroup.ORANGE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Community Chest",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHEST,
        ),
        GameSpace(
            name="Tennessee Ave",
            value=180,
            group=PropertyGroup.ORANGE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="New York Ave",
            value=200,
            group=PropertyGroup.ORANGE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Free Parking",
            value=0,
            group=None,
            type=GameSpaceTypes.FREE,
        ),
        GameSpace(
            name="Kentucky Ave",
            value=220,
            group=PropertyGroup.RED,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Chance",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHANCE,
        ),
        GameSpace(
            name="Indiana Ave",
            value=220,
            group=PropertyGroup.RED,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Illinois Ave",
            value=240,
            group=PropertyGroup.RED,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="B & O Railroad",
            value=200,
            group=PropertyGroup.RAILROAD,
            type=GameSpaceTypes.RAILROAD,
        ),
        GameSpace(
            name="Atlantic Ave",
            value=260,
            group=PropertyGroup.YELLOW,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Ventnor Ave",
            value=260,
            group=PropertyGroup.YELLOW,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Water Works",
            value=150,
            group=None,
            type=GameSpaceTypes.TAX,
        ),
        GameSpace(
            name="Marvin Gardens",
            value=280,
            group=PropertyGroup.YELLOW,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Go to Jail",
            value=0,
            group=None,
            type=GameSpaceTypes.GO_TO_JAIL,
        ),
        GameSpace(
            name="Pacific Ave",
            value=300,
            group=PropertyGroup.GREEN,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="North Carolina Ave",
            value=300,
            group=PropertyGroup.GREEN,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Community Chest",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHEST,
        ),
        GameSpace(
            name="Pennsylvania Ave",
            value=320,
            group=PropertyGroup.GREEN,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Short Line",
            value=200,
            group=PropertyGroup.RAILROAD,
            type=GameSpaceTypes.RAILROAD,
        ),
        GameSpace(
            name="Chance",
            value=0,
            group=None,
            type=GameSpaceTypes.DRAW_CHANCE,
        ),
        GameSpace(
            name="Park Place",
            value=350,
            group=PropertyGroup.BLUE,
            type=GameSpaceTypes.PROPERTY,
        ),
        GameSpace(
            name="Luxury Tax",
            value=75,
            group=None,
            type=GameSpaceTypes.TAX,
        ),
        GameSpace(
            name="Boardwalk",
            value=400,
            group=PropertyGroup.BLUE,
            type=GameSpaceTypes.PROPERTY,
        ),
    ]
    for space in default_spaces:
        game.add_space(space)

    game.cc_cards = [
        Card(title="Advance to Go (Collect $200)", type=CardTypes.COMMUNITY_CHEST),
        Card(title="From sale of stock, you get $45", type=CardTypes.COMMUNITY_CHEST),
        Card(title="You inherit $100", type=CardTypes.COMMUNITY_CHEST),
        Card(title="Pay hospital $100", type=CardTypes.COMMUNITY_CHEST),
        Card(
            title="Grand Opera Opening. Collect $50 from every player for opening night seats.",
            type=CardTypes.COMMUNITY_CHEST,
        ),
        Card(title="Income Tax Refund. Collect $20", type=CardTypes.COMMUNITY_CHEST),
        Card(title="Receive for services, $20", type=CardTypes.COMMUNITY_CHEST),
        Card(title="Doctor's Fee. Pay $50", type=CardTypes.COMMUNITY_CHEST),
        Card(
            title="Go to jail. Go directly to jail. Do not pass go. Do not collect $200",
            type=CardTypes.COMMUNITY_CHEST,
        ),
        Card(title="Bank error in your favor. Collect $200", type=CardTypes.COMMUNITY_CHEST),
        Card(title="Xmas fund matures. Collect $100", type=CardTypes.COMMUNITY_CHEST),
        Card(title="Life insurance matures. Collect $100", type=CardTypes.COMMUNITY_CHEST),
        Card(
            title="Get out of jail free. (This card may be kept until needed, or sold)",
            type=CardTypes.COMMUNITY_CHEST,
        ),
        Card(title="Pay School tax of $150", type=CardTypes.COMMUNITY_CHEST),
        Card(
            title="You have won 2nd price in a beauty contest. Collect $10",
            type=CardTypes.COMMUNITY_CHEST,
        ),
        Card(
            title="You are assessed for street repairs. $40 per house, $115 per hotel",
            type=CardTypes.COMMUNITY_CHEST,
        ),
    ]

    game.chance_cards = [
        Card(
            title="You have been elected chairman of the board. Pay each player $50",
            type=CardTypes.CHANCE,
        ),
        Card(title="Your building and loan matures. Collect $150", type=CardTypes.CHANCE),
        Card(
            title="Get out of jail free. This card may be kept until needed, or sold",
            type=CardTypes.CHANCE,
        ),
        Card(title="Bank Pays you dividend of $50", type=CardTypes.CHANCE),
        Card(title="Pay poor tax of $15", type=CardTypes.CHANCE),
        Card(
            title="Take a ride on the Reading. If you pass go, collect $200", type=CardTypes.CHANCE
        ),
        Card(title="Advance to go (Collect $200)", type=CardTypes.CHANCE),
        Card(
            title="Advance to St. Charles Place. If you pass go, collect $200",
            type=CardTypes.CHANCE,
        ),
        Card(title="Go back 3 spaces", type=CardTypes.CHANCE),
        Card(
            title="Take a walk on the Boardwalk. Advance token to Boardwalk", type=CardTypes.CHANCE
        ),
        Card(
            title=(
                "Advance token to the nearest Railroad and pay owner twice the rental to "
                "which he/she is otherwise entitled. If Railroad if UNOWNED, you may purchase "
                "it from the bank"
            ),
            type=CardTypes.CHANCE,
        ),
        Card(
            title=(
                "Advance token to the nearest Railroad and pay owner twice the rental to "
                "which he/she is otherwise entitled. If Railroad if UNOWNED, you may purchase "
                "it from the bank"
            ),
            type=CardTypes.CHANCE,
        ),
        Card(
            title=(
                "Advance token to the nearest utility. If UNOWNED you may buy if from the bank. "
                "If OWNED, throw dice and pay owner a total ten times the amount thrown"
            ),
            type=CardTypes.CHANCE,
        ),
        Card(title="Advance to Illinois Ave", type=CardTypes.CHANCE),
        Card(
            title="Go directly to jail. Do not pass GO. Do not collect $200", type=CardTypes.CHANCE
        ),
        Card(
            title=(
                "Make general repairs on all your property. For each house pay $25, "
                "for each hotel $100"
            ),
            type=CardTypes.CHANCE,
        ),
    ]
    game.shuffle_cards()

    player_1 = Player(name="Chris")
    game.add_player(player_1)
    player_2 = Player(name="Benny")
    game.add_player(player_2)
    # TODO: allow player to HOLD GOOJ-free card
    return game


if __name__ == "__main__":  # pragma: no cover
    game = setup_game()
    game.play()
