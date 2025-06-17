from typing import TYPE_CHECKING
from pygame.color import Color
from common.constant import HTMLColor
from common.math import Vector2
from core.ant import Ant

if TYPE_CHECKING:
    from core.world import World


class NormalAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.GREEN), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()
        world.flip_tile(self.position)
        self.move(steps, world)


class ReversedAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.ORANGE), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()

        steps *= -1

        world.flip_tile(self.position)
        self.move(steps, world)


class TransposedAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.LIGHT_BLUE), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()

        x, y = steps

        world.flip_tile(self.position)
        self.move(Vector2(y, x), world)


class DoubleFlipperAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.VIOLET), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()
        world.flip_tile(self.position, 2)
        self.move(steps, world)
