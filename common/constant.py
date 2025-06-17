from enum import Enum, StrEnum

from common.math import Vector2


class HTMLColor(StrEnum):
    # Define the color constants
    WHITE = "#F0EBEB"
    RED = "#E61414"
    LIGHT_GREEN = "#61FD3A"
    GREEN = "#23CE09"
    LIGHT_BLUE = "#50BAE7"
    BLUE = "#1B07ED"
    VIOLET = "#9C20E9"
    MAGENTA = "#B70BB1"
    PURPLE = "#7A0461"
    YELLOW = "#FAFF14"
    ORANGE = "#F43A01"
    BLACK = "#131111"


class DirectionVector(Enum):
    # Define direction constants
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def as_vector2(self) -> Vector2:
        return Vector2(*self.value)
