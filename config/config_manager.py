import json
from pathlib import Path
from pydantic import BaseModel, PositiveInt


class AntConfig(BaseModel):
    limit: int
    types: dict[str, int]


class TileConfig(BaseModel):
    resolution: PositiveInt


class WorldConfig(BaseModel):
    fps: PositiveInt
    grid_size: tuple[PositiveInt, PositiveInt]
    window_size: tuple[PositiveInt, PositiveInt]
    background_color: str
    ant_config: AntConfig
    tile_config: TileConfig


def default(path: str | Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    ant_config = AntConfig(limit=-1, types={"NormalAnt": 5})
    tile_config = TileConfig(resolution=15)
    world_config = WorldConfig(
        fps=60,
        grid_size=(30, 30),
        window_size=(500, 500),
        background_color="#FFFFFF",
        ant_config=ant_config,
        tile_config=tile_config,
    )

    with open(path, "w") as file:
        json.dump(world_config.model_dump(), file, indent=4)

    return world_config


def load_config(path: str | Path) -> WorldConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Cannot find {path.absolute()}.")

    with open(path) as file:
        config = json.load(file)

    return WorldConfig(**config)


def get() -> WorldConfig:
    path = "./settings/dev-settings.json"
    try:
        config = load_config(path)
    except FileNotFoundError:
        config = default(path)

    return config
