from typing import TYPE_CHECKING
from core.registry import AntRegistry
from pygame import Color
from core.ant import Ant
from common.constant import HTMLColor
from common.math import Vector2
import random

if TYPE_CHECKING:
    from core.world import World


class MotherAnt(Ant):
    def __init__(self, position: Vector2):
        super().__init__(Color(HTMLColor.BLUE), position)
        self.step_to_spawn = 5
        self.cooldown = 0

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        dx, dy = tile.get_direction()

        if self.cooldown != self.step_to_spawn:
            self.cooldown += 1
        else:
            new_ant = AntRegistry.at(random.randint(0, len(AntRegistry.all()) - 1))[1]
            if len(world.ants) < world.config.ant_config.limit:
                world.ants.append(new_ant(self.position))
            self.cooldown = 0

        world.flip_tile(self.position, 5)
        self.move(Vector2(dx, dy), world)


class RadiationAnt(Ant):
    def __init__(self, position: Vector2):
        super().__init__(Color(HTMLColor.PURPLE), position)
        self.live = 500

    def _tile(self, x: int, y: int, grid_size: Vector2) -> Vector2:
        x = x % grid_size.x
        y = y % grid_size.y
        return Vector2(x, y)

    def update(self, world: "World"):
        self.live -= 1
        if self.live == 0:
            world.ants.remove(self)
        tile = world.get_tile(self.position)
        dx, dy = tile.get_direction()

        x, y = self.position
        world.flip_tile(self.position)
        world.flip_tile(self._tile(x + 1, y, world.grid_size))
        world.flip_tile(self._tile(x - 1, y, world.grid_size))
        world.flip_tile(self._tile(x, y + 1, world.grid_size))
        world.flip_tile(self._tile(x, y - 1, world.grid_size))
        world.flip_tile(self._tile(x - 1, y - 1, world.grid_size))
        world.flip_tile(self._tile(x + 1, y - 1, world.grid_size))
        world.flip_tile(self._tile(x - 1, y + 1, world.grid_size))
        world.flip_tile(self._tile(x + 1, y + 1, world.grid_size))

        self.move(Vector2(dx, dy), world)
