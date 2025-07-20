import os
import json
import sys
import random
from typing import Callable
import pygame
from common.event import UI_BUTTON_CLICKED
from config import config_manager
from core.world import World
from gui.menu import FrontMenu, EditorMenu


class MainWindow:
    conf = config_manager.get()

    def __init__(self):
        self.random_seed = self.conf.random_seed
        if self.random_seed is None:
            self.random_seed = random.randrange(sys.maxsize)
        random.seed(self.random_seed)

        pygame.init()
        self.resolution = self.conf.tile_config.resolution
        self.grid_size = self.conf.grid_size

        self.window_size = self._get_window_size()
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.renderer = []

        self.world = World()
        self.world.running = True
        self.p = FrontMenu(self)
        self._menu = True

    def add_renderer(self, renderer: Callable[["MainWindow"], None]):
        self.renderer.append(renderer)

    def render(self):
        for to_render in self.renderer:
            to_render(self)
        if self._menu:
            self.p.render(self.screen)

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
            elif event.type == UI_BUTTON_CLICKED:
                if event.dict.get("buttonId") == "New":
                    self.p = EditorMenu(self)
                    self.world.running = False
                elif event.dict.get("buttonId") == "Load":
                    path = os.path.join(os.getcwd(), "world_map.json")
                    if not os.path.exists(path):
                        print("No world_map.json found.")
                    else:
                        with open(path, "r") as f:
                            data = json.load(f)
                        self.world.load(data)
                        self._menu = False
                        print("Loaded world from world_map.json")
                elif event.dict.get("buttonId") == "Quit":
                    self.running = False
                else:
                    print(event.buttonId)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self._menu:
                    self.p = FrontMenu(self)
                    self._menu = not self._menu

            if self._menu:
                self.p.update(event)
