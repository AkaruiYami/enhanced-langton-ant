import random
from typing import Callable
import pygame
from config import config_manager
from core.world import World


class MainWindow:
    conf = config_manager.get()

    def __init__(self):
        random.seed(self.conf.random_seed)
        pygame.init()
        self.resolution = self.conf.tile_config.resolution
        self.grid_size = self.conf.grid_size

        self.window_size = self._get_window_size()
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.renderer = []

        self.world = World()

    def add_renderer(self, renderer: Callable[["MainWindow"], None]):
        self.renderer.append(renderer)

    def render(self):
        for to_render in self.renderer:
            to_render(self)

    def run(self):
        fps = self.conf.fps
        bg_color = self.conf.background_color
        while self.running:
            self.clock.tick(fps)
            self._handle_event()
            self.screen.fill(bg_color)

            self.world.update()

            self.render()

            pygame.display.flip()
        pygame.quit()

    def _get_window_size(self) -> tuple[int, int]:
        size = self.conf.window_size
        size_base_on_grid = (
            self.grid_size[0] * self.resolution,
            self.grid_size[1] * self.resolution,
        )
        return max(size, size_base_on_grid)

    def _handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
