from random import randint

from pydantic import BaseModel

from models.constants import RollResultCodes


class Player(BaseModel):
    name: str
    position: int = 0
    cash: int = 1500
    in_jail: bool = False
    prev_double: list[bool] = [False, False, False]
    jail_count: int = 0

    def roll_die(self) -> tuple[int, int]:
        return randint(1, 6), randint(1, 6)

    def roll(self) -> int:
        roll_1, roll_2 = self.roll_die()
        self.prev_double.pop(0)
        if roll_1 == roll_2:
            self.prev_double.append(True)
            if self.in_jail:
                return RollResultCodes.JAIL_DOUBLE
            if all(self.prev_double):
                return RollResultCodes.THIRD_DOUBLE
        else:
            self.prev_double.append(False)
            if self.in_jail and self.jail_count > 0:
                self.jail_count -= 1
                return 0
        return roll_1 + roll_2
