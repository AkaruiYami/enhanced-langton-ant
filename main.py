from engine import autoload
from gui import MainWindow
from gui.renderer import draw_ant, draw_ant_count, draw_overlay, draw_tile


def main():
    autoload.load_py_files("./assets/entity/")
    autoload.load_py_files("./mods/")

    app = MainWindow()

    app.add_renderer(draw_tile)
    app.add_renderer(draw_overlay)
    app.add_renderer(draw_ant)
    app.add_renderer(draw_ant_count)

    app.run()


if __name__ == "__main__":
    main()
