from common.math import Vector2
from config import config_manager
from core.registry import AntRegistry, TileRegistry
from core.tile import Tile


class World:
    config = config_manager.get()

    def __init__(self):
        self.ants = []
        self.tiles = []
        self.grid_size = Vector2(*self.config.grid_size)

        self._init_tiles()
        self._init_ants()

    def update(self):
        pass

    def get_tile(self, position: Vector2) -> Tile:
        x, y = position
        return self.tiles[y][x]

    def _init_tiles(self):
        x, y = self.grid_size
        for _ in range(y):
            self.tiles.append([TileRegistry.at(0)[1] for _ in range(x)])

    def _init_ants(self):
        ant_conf = self.config.ant_config
        for name, count in ant_conf.types.items():
            if name not in AntRegistry.names():
                print(f"Ant type of {name} does not exist. Skip adding.")
                continue
            self.ants.extend([AntRegistry.get(name)] * count)
