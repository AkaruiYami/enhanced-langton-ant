import sys
from pathlib import Path


def is_bundled() -> bool:
    return getattr(sys, "_MEIPASS", None) is not None


def get_bundle_dir() -> Path:
    if is_bundled():
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_exe_dir() -> Path:
    if is_bundled():
        return Path(sys.executable).parent
    return Path.cwd()


def get_settings_path() -> Path:
    return get_bundle_dir() / "settings" / "dev-settings.json"


def get_assets_dir() -> Path:
    return get_bundle_dir() / "assets" / "entity"


def get_mods_dir() -> Path:
    return get_bundle_dir() / "mods"


def get_data_dir() -> Path:
    data_dir = get_exe_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
