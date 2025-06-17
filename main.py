# TODO: Automatically call the registry
import engine
from gui import MainWindow
from gui.renderer import draw_ant, draw_tile


def main():
    app = MainWindow()

    app.add_renderer(draw_tile)
    app.add_renderer(draw_ant)

    app.run()


if __name__ == "__main__":
    main()
