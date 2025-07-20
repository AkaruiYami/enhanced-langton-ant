from common.math import Vector2
from config import config_manager
from core.ant import Ant
from core.registry import AntRegistry, TileRegistry
from core.tile import Tile


class World:
    config = config_manager.get()

    def __init__(self):
        self.reset()
        self.running = False

    def reset(self):
        self.ants: list[Ant] = []
        self.tiles: list[list[Tile]] = []
        self.grid_size = Vector2(*self.config.grid_size)

        self._init_tiles()
        self._init_ants()

    def update(self):
        if self.running:
            for ant in self.ants:
                ant.update(self)

    def flip_tile(self, position: Vector2 | tuple[int, int] | list[int], n: int = 1):
        x, y = position
        curr_tile = self.get_tile(position)
        curr_id = TileRegistry.names().index(curr_tile.__class__.__name__)
        new_id = (curr_id + n) % len(TileRegistry.all())
        self.tiles[y][x] = TileRegistry.at(new_id)[1]()

    def get_tile(self, position: Vector2 | tuple[int, int] | list[int]) -> Tile:
        x, y = position
        return self.tiles[y][x]

    @classmethod
    def point_to_grid(cls, point: Vector2 | tuple[int, int] | list[int]) -> Vector2:
        point = Vector2(*point)
        return point / cls.config.tile_config.resolution

    @classmethod
    def grid_to_point(cls, grid_coor: Vector2 | tuple[int, int] | list[int]) -> Vector2:
        point = Vector2(*grid_coor)
        return point * cls.config.tile_config.resolution

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
            self.ants.extend([ant(mid) for _ in range(count)])

    def load(self, data: dict):
        self.running = False
        self.reset()
        self.ants.clear()
        self.tiles = [[TileRegistry.at(0)[1]() for _ in range(int(self.grid_size[0]))] for _ in range(int(self.grid_size[1]))]
        # Load ants
        for ant_info in data.get("ants", []):
            ant_cls = AntRegistry.get(ant_info["type"])
            if ant_cls:
                pos = ant_info["position"]
                self.ants.append(ant_cls(pos))
        # Load tiles
        for tile_info in data.get("tiles", []):
            tile_cls = TileRegistry.get(tile_info["type"])
            if tile_cls:
                x, y = tile_info["position"]
                self.tiles[y][x] = tile_cls()
        self.running = True
