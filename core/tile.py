import abc
from pygame.color import Color
from common.math import Vector2
from core.registry import TileRegistry


class Tile(abc.ABC):
    def __init__(self, color: Color):
        self.color = color

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        TileRegistry.register(cls.__name__, cls)

    @abc.abstractmethod
    def get_direction(self) -> Vector2:
        pass
