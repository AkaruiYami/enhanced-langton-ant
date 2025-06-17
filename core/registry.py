from typing import Tuple, Type, TypeVar, Generic, Dict, Optional

from core.ant import Ant
from core.tile import Tile

T = TypeVar("T")


class BaseRegistry(Generic[T]):
    _registry = {}

    @classmethod
    def register(cls, name: str, item_cls: Type) -> Type:
        cls._registry[name] = item_cls
        return item_cls

    @classmethod
    def at(cls, index: int) -> Tuple[str, Type]:
        if not cls._registry:
            raise IndexError(f"Registry in {cls.__name__} is empty.")
        name, tile = list(cls._registry.items())[index]
        return name, tile

    @classmethod
    def get(cls, name: str) -> Optional[Type]:
        return cls._registry.get(name)

    @classmethod
    def all(cls) -> Dict[str, Type]:
        return cls._registry

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._registry.keys())


class TileRegistry(BaseRegistry[Tile]):
    _registry: Dict[str, Type[Tile]] = {}


class AntRegistry(BaseRegistry[Ant]):
    _registry: Dict[str, Type[Ant]] = {}
