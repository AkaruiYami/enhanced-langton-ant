from pygame import Color
from common.constant import HTMLColor
from common.math import Vector2
from core.tile import Tile


class YellowTile(Tile):
    def __init__(self):
        super().__init__(Color(HTMLColor.YELLOW))

    def get_direction(self) -> Vector2:
        return Vector2(1, 1)
