import random
from pygame.color import Color
from common.constant import DirectionVector, HTMLColor

from core.tile import Tile


class WhiteTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.WHITE))

    def get_direction(self):
        return random.choice([v.as_vector2() for v in DirectionVector])


class BlackTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.BLACK))

    def get_direction(self):
        return DirectionVector.LEFT.as_vector2()


class GreenTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.GREEN))

    def get_direction(self):
        return DirectionVector.RIGHT.as_vector2()


class RedTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.RED))

    def get_direction(self):
        return DirectionVector.DOWN.as_vector2()


class MagentaTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.MAGENTA))

    def get_direction(self):
        return random.choice(
            [
                DirectionVector.DOWN.as_vector2(),
                DirectionVector.UP.as_vector2(),
            ]
        )
