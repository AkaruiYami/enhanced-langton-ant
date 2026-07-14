import logging
import pathlib
from dataclasses import dataclass
from importlib import util

logger = logging.getLogger(__name__)

_loaded_paths: set[pathlib.Path] = set()


@dataclass(slots=True)
class LoadStats:
    loaded: int = 0
    skipped: int = 0
    failed: int = 0


def load_py_files(directory: str | pathlib.Path) -> LoadStats:
    stats = LoadStats()
    path = pathlib.Path(directory)

    for file in path.glob("*.py"):
        if file.name.startswith("_"):
            stats.skipped += 1
            continue

        module_path = file.absolute()

        if module_path in _loaded_paths:
            logger.debug("Already loaded: %s", file.name)
            stats.skipped += 1
            continue

        module_name = file.stem

        try:
            spec = util.spec_from_file_location(module_name, module_path)
            if spec is None or spec.loader is None:
                logger.warning("Cannot build spec for %s", file.name)
                stats.skipped += 1
                continue

            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _loaded_paths.add(module_path)
            logger.debug("Loaded: %s", module_name)
            stats.loaded += 1
        except Exception as e:
            logger.error("Failed to load %s: %s", file.name, e)
            stats.failed += 1

    return stats


def loaded_modules() -> frozenset[pathlib.Path]:
    return frozenset(_loaded_paths)
