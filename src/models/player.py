from random import randint

import click
from pydantic import BaseModel


class Player(BaseModel):
    name: str
    position: int = 0
    cash: int = 1500
    in_jail: bool = False
    prev_double: list[bool] = [False, False, False]
    jail_count: int = 0

    def roll(self) -> int:
        roll_1 = randint(1, 6)
        roll_2 = randint(1, 6)
        if roll_1 == roll_2:
            self.prev_double.append(True)
        else:
            self.prev_double.append(False)
        if all(self.prev_double):
            click.echo("3rd consecutive double, go to jail, fool!")
            return 0
        return roll_1 + roll_2
