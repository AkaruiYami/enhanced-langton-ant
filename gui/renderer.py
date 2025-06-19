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


def draw_overlay(app: "MainWindow"):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_o]:
        win_rect = pygame.Rect(0, 0, app.window_size[0], app.window_size[1])
        ruf = pygame.Surface(win_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(ruf, pygame.Color(5, 5, 5, 220), win_rect)
        app.screen.blit(ruf, (0, 0))


def draw_ant_count(app: "MainWindow"):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_c]:
        n_ant = len(app.world.ants)
        font = pygame.font.Font(None, 25)
        text = font.render(f"Ant Count: {n_ant}", True, pygame.Color(0, 0, 0))
        surf = pygame.Surface(text.get_rect().size, pygame.SRCALPHA)
        surf.fill(pygame.Color(200, 200, 200, 150))
        surf.blit(text, (0, 0))
        app.screen.blit(surf, (0, 0))
