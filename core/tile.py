import abc
from pygame.color import Color
from common.math import Vector2


class Tile(abc.ABC):
    def __init__(self, color: Color):
        self.color = color

    @abc.abstractmethod
    def get_direction(self) -> Vector2:
        pass
