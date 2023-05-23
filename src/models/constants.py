from enum import StrEnum


class GameSpaceTypes(StrEnum):
    DRAW_CHEST = "draw-chest"
    DRAW_CHANCE = "draw-chance"
    FREE = "free"
    GO_TO_JAIL = "go-to-jail"
    JAIL = "jail"
    PROPERTY = "property"
    RAILROAD = "railroad"
    TAX = "tax"
    TAX_INCOME = "tax-income"


class PropertyGroup(StrEnum):
    BLUE = "blue"
    GREEN = "green"
    LIGHT_BLUE = "light-blue"
    ORANGE = "orange"
    RAILROAD = "railroad"
    RED = "red"
    PURPLE = "purple"
    VIOLET = "violet"
    YELLOW = "yellow"


class PropertyStatus(StrEnum):
    OWNED = "owned"
    VACANT = "vacant"
