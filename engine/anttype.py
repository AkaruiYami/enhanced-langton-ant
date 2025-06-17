from typing import TYPE_CHECKING
from pygame.color import Color
from common.constant import HTMLColor
from common.math import Vector2
from core.ant import Ant
from core.registry import AntRegistry

if TYPE_CHECKING:
    from core.world import World


class NormalAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.GREEN), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()
        self.move(steps)


class ReversedAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.ORANGE), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()

        steps *= -1

        self.move(steps)


class TransposedAnt(Ant):
    def __init__(self, position):
        super().__init__(Color(HTMLColor.LIGHT_BLUE), position)

    def update(self, world: "World"):
        tile = world.get_tile(self.position)
        steps = tile.get_direction()

        x, y = steps

        self.move(Vector2(y, x))


AntRegistry.register("NormalAnt", NormalAnt)
AntRegistry.register("ReversedAnt", ReversedAnt)
AntRegistry.register("TransposedAnt", TransposedAnt)
