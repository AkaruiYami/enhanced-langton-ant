from typing import Tuple, TypeVar, Generic, Type, Dict, Optional

from core.ant import Ant
from core.tile import Tile

T = TypeVar("T")


class BaseRegistry(Generic[T]):
    _registry = {}

    @classmethod
    def register(cls, name: str, item_cls: Type[T]) -> Type[T]:
        cls._registry[name] = item_cls
        return item_cls

    @classmethod
    def at(cls, index: int) -> Tuple[str, Type[T]]:
        if not cls._registry:
            raise IndexError(f"Registry in {cls.__name__} is empty.")
        return list(cls._registry.items())[index]

    @classmethod
    def get(cls, name: str) -> Optional[Type[T]]:
        return cls._registry.get(name)

    @classmethod
    def all(cls) -> Dict[str, Type[T]]:
        return cls._registry

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._registry.keys())


class TileRegistry(BaseRegistry[Tile]):
    _registry: Dict[str, Tile] = {}


class AntRegistry(BaseRegistry[Ant]):
    _registry: Dict[str, Ant] = {}
