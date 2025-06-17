from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from pygame.color import Color
from common.math import Vector2
from core.registry import AntRegistry

if TYPE_CHECKING:
    from core.world import World


class Ant(ABC):
    def __init__(self, color: Color, position: Optional[Vector2] = None):
        if position is None:
            position = Vector2(0, 0)
        self.color = color
        self.position = position

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        AntRegistry.register(cls.__name__, cls)

    def move(self, steps: Vector2, world: "World"):
        dx, dy = steps
        new_x = (self.position[0] + dx) % world.grid_size[0]
        new_y = (self.position[1] + dy) % world.grid_size[1]
        self.position = (new_x, new_y)

    @abstractmethod
    def update(self, world: "World"):
        pass
