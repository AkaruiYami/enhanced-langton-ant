from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from pygame.color import Color
from common.math import Vector2

if TYPE_CHECKING:
    from core.world import World


class Ant(ABC):
    def __init__(self, color: Color, position: Optional[Vector2] = None):
        if position is None:
            position = Vector2(0, 0)
        self.color = color
        self.position = position

    def move(self, steps: Vector2):
        self.position += steps

    @abstractmethod
    def update(self, world: "World"):
        pass
