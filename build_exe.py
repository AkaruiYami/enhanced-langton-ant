import PyInstaller.__main__
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PyInstaller.__main__.run([
    str(ROOT / "main.py"),
    "--name=EnhancedLangtonAnt",
    "--windowed",
    "--onefile",
    "--noconfirm",
    f"--distpath={ROOT / 'build' / 'dist'}",
    f"--workpath={ROOT / 'build' / 'build_tmp'}",
    f"--specpath={ROOT / 'build'}",
    f"--add-data={ROOT / 'assets'}:assets",
    f"--add-data={ROOT / 'mods'}:mods",
    f"--add-data={ROOT / 'settings'}:settings",
    "--hidden-import=engine",
    "--hidden-import=engine.autoload",
    "--hidden-import=common",
    "--hidden-import=common.constant",
    "--hidden-import=common.math",
    "--hidden-import=common.paths",
    "--hidden-import=config",
    "--hidden-import=config.config_manager",
    "--hidden-import=core",
    "--hidden-import=core.ant",
    "--hidden-import=core.tile",
    "--hidden-import=core.registry",
    "--hidden-import=core.world",
    "--hidden-import=gui",
    "--hidden-import=gui.component",
    "--hidden-import=gui.dialog",
    "--hidden-import=gui.layout",
    "--hidden-import=gui.menu",
    "--hidden-import=gui.renderer",
    "--hidden-import=gui.MainWindow",
])
