import random
from pygame.color import Color
from common.constant import DirectionVector, HTMLColor
from core.registry import TileRegistry
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


TileRegistry.register("WhiteTile", WhiteTile)
TileRegistry.register("BlackTile", BlackTile)
