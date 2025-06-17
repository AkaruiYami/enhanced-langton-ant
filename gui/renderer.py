from typing import TYPE_CHECKING
import pygame


if TYPE_CHECKING:
    from gui import MainWindow


def draw_tile(app: "MainWindow"):
    for y in range(app.grid_size[1]):
        for x in range(app.grid_size[0]):
            tile = app.world.get_tile((x, y))
            rect = pygame.Rect(
                x * app.resolution,
                y * app.resolution,
                app.resolution,
                app.resolution,
            )
            pygame.draw.rect(app.screen, tile.color, rect)


def draw_ant(app: "MainWindow"):
    for ant in app.world.ants:
        ax, ay = ant.position
        center_x = ax * app.resolution + app.resolution // 2
        center_y = ay * app.resolution + app.resolution // 2
        radius = app.resolution // 2
        pygame.draw.circle(app.screen, ant.color, (center_x, center_y), radius)
