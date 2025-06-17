from common.math import Vector2
from config import config_manager
from core.ant import Ant
from core.registry import AntRegistry, TileRegistry
from core.tile import Tile


class World:
    config = config_manager.get()

    def __init__(self):
        self.ants: list[Ant] = []
        self.tiles: list[list[Tile]] = []
        self.grid_size = Vector2(*self.config.grid_size)

        self._init_tiles()
        self._init_ants()

    def update(self):
        pass

    def get_tile(self, position: Vector2 | tuple[int, int] | list[int]) -> Tile:
        x, y = position
        return self.tiles[y][x]

    def _init_tiles(self):
        x, y = self.grid_size
        for _ in range(y):
            new_tile = TileRegistry.at(0)[1]
            self.tiles.append([new_tile() for _ in range(x)])

    def _init_ants(self):
        ant_conf = self.config.ant_config
        for name, count in ant_conf.types.items():
            ant = AntRegistry.get(name)
            if ant is None:
                print(f"Cannot find {name} in AntRegistry. Skipping.")
                continue
            if count < 0:
                raise ValueError(f"The number of {name} cannot be below 0.")

            mid = self.grid_size / 2
            self.ants.extend([ant(mid)] * count)
