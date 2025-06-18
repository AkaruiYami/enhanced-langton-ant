from engine import autoload
from gui import MainWindow
from gui.renderer import draw_ant, draw_tile


def main():
    autoload.load_py_files("./assets/entity/")
    autoload.load_py_files("./mods/")

    app = MainWindow()

    app.add_renderer(draw_tile)
    app.add_renderer(draw_ant)

    app.run()


if __name__ == "__main__":
    main()
