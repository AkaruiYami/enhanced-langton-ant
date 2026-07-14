from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame
from common import Alignment
from common.constant import HTMLColor
from common.math import Vector2
from core.world import World
from gui.component import Button
from gui.layout import Column, Row
import json
import os

from core.registry import AntRegistry, TileRegistry

if TYPE_CHECKING:
    from gui import MainWindow


def _construct_button(label: str) -> Button:
    button = Button(
        label,
        pygame.Color(HTMLColor.WHITE),
        pygame.Color(HTMLColor.PURPLE),
        pygame.Color(HTMLColor.VIOLET),
        pygame.font.Font(None, 25),
        True,
        rect=pygame.Rect(0, 0, 200, 50),
    )
    return button


class Menu(ABC):
    def __init__(self, parent: "MainWindow") -> None:
        self.parent = parent

    @abstractmethod
    def render(self, surface: pygame.Surface, position: tuple[int, int]): ...

    @abstractmethod
    def update(self, event: pygame.event.EventType): ...


class FrontMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.surface = self._construct_menu()

    def _construct_menu(self):
        row = Row(alignment=Alignment.CENTER, rect=self.parent.screen.get_rect())
        column = Column(spacing=10, alignment=Alignment.CENTER, rect=row.get_rect())

        self._new_button = _construct_button("New")
        self._load_button = _construct_button("Load")
        self._quit_button = _construct_button("Quit")

        column.rect.width = max(
            self._new_button.rect.width,
            self._load_button.rect.width,
            self._quit_button.rect.width,
        )

        row.push(column)
        column.push(self._new_button)
        column.push(self._load_button)
        column.push(self._quit_button)

        return row

    def render(self, surface: pygame.Surface, position=(0, 0)):
        bg = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        bg.fill(HTMLColor.BLACK + "80")

        surface.blit(bg, (0, 0))
        self.surface.render(surface, position)

    def update(self, event):
        self.surface.update(event)


# TODO: Andd all the ant type into selection panel
# block the grid underneath the panel from accidental click
# make this menu appeares when user choose 'New'
# add save option
# load the world using the save file. instead
class EditorMenu(Menu):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.surface = pygame.Surface(parent.screen.get_size())
        self._is_ant_panel_active = False
        self.selected_entity = None
        self._entity_types = self._load_entity_types()
        self._save_button = _construct_button("Save")
        self._load_button = _construct_button("Load")
        self._panel_buttons: list[pygame.Rect] = []
        self._panel_rect = pygame.Rect(0, 0, 0, 0)

    def _load_entity_types(self):
        from core.registry import AntRegistry, TileRegistry

        return {
            "ant": AntRegistry.names(),
            "tile": TileRegistry.names(),
        }

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.surface.fill(HTMLColor.WHITE)
        self._render_entities()
        self._render_grid_lines()
        self._render_ghost()
        if self._is_ant_panel_active:
            self._render_selection_panel()
        self._render_buttons()
        surface.blit(self.surface, position)

    def update(self, event: pygame.event.EventType):
        if self._is_ant_panel_active:
            self._handle_panel_event(event)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            coor = pygame.mouse.get_pos()
            if self._panel_rect.collidepoint(coor):
                return
            grid = World.point_to_grid(coor)
            if self._save_button.rect.collidepoint(coor):
                self._save_map()
                return
            if self._load_button.rect.collidepoint(coor):
                self._load_map()
                return
            if event.button == 3:
                self._remove_entity_at(grid)
            elif event.button == 1 and self.selected_entity:
                self._place_entity(grid)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._is_ant_panel_active = not self._is_ant_panel_active
            elif event.key == pygame.K_ESCAPE:
                self.selected_entity = None

    def _place_entity(self, grid):
        gx, gy = int(grid.x), int(grid.y)
        if self.selected_entity in self._entity_types["ant"]:
            ant = AntRegistry.get(self.selected_entity)
            self.parent.world.ants.append(ant(grid))
        elif self.selected_entity in self._entity_types["tile"]:
            tile = TileRegistry.get(self.selected_entity)
            self.parent.world.tiles[gy][gx] = tile()

    def _remove_entity_at(self, grid):
        gx, gy = int(grid.x), int(grid.y)
        self.parent.world.ants = [
            a for a in self.parent.world.ants
            if int(a.position[0]) != gx or int(a.position[1]) != gy
        ]
        tiles = self.parent.world.tiles
        if 0 <= gy < len(tiles) and 0 <= gx < len(tiles[0]):
            tiles[gy][gx] = TileRegistry.at(0)[1]()

    def _render_grid_lines(self):
        grid_size = Vector2(*self.parent.conf.grid_size)
        cell_size = self.parent.conf.tile_config.resolution
        grid_size *= cell_size
        for x in range(0, grid_size.x, cell_size):
            pygame.draw.line(
                self.surface,
                HTMLColor.BLACK,
                (x, 0),
                (x, grid_size.y),
            )
        for y in range(0, grid_size.y, cell_size):
            pygame.draw.line(
                self.surface,
                HTMLColor.BLACK,
                (0, y),
                (grid_size.x, y),
            )

    def _render_ghost(self):
        if self.selected_entity is None or self._is_ant_panel_active:
            return
        coor = pygame.mouse.get_pos()
        if self._panel_rect.collidepoint(coor):
            return
        cell_size = self.parent.conf.tile_config.resolution
        grid = World.point_to_grid(coor)
        gx, gy = int(grid.x), int(grid.y)
        grid_w = self.parent.conf.grid_size[0]
        grid_h = self.parent.conf.grid_size[1]
        if gx < 0 or gx >= grid_w or gy < 0 or gy >= grid_h:
            return
        ghost = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        entity_cls = None
        if self.selected_entity in self._entity_types["ant"]:
            entity_cls = AntRegistry.get(self.selected_entity)
        elif self.selected_entity in self._entity_types["tile"]:
            entity_cls = TileRegistry.get(self.selected_entity)
        if entity_cls is None:
            return
        color = entity_cls().color
        alpha_color = pygame.Color(color.r, color.g, color.b, 128)
        if self.selected_entity in self._entity_types["ant"]:
            pygame.draw.circle(ghost, alpha_color, (cell_size // 2, cell_size // 2), cell_size // 2)
        else:
            pygame.draw.rect(ghost, alpha_color, (0, 0, cell_size, cell_size))
        self.surface.blit(ghost, (gx * cell_size, gy * cell_size))

    def _render_entities(self):
        cell_size = self.parent.conf.tile_config.resolution
        tiles = self.parent.world.tiles
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * cell_size,
                    y * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(self.surface, tile.color, rect)

        for ant in self.parent.world.ants:
            ax, ay = ant.position
            center_x = ax * cell_size + cell_size // 2
            center_y = ay * cell_size + cell_size // 2
            radius = cell_size // 2
            pygame.draw.circle(self.surface, ant.color, (center_x, center_y), radius)

    def _render_selection_panel(self):
        _size = self.surface.get_size()
        height = _size[1] // 4
        width = _size[0]
        panel_y = _size[1] - height

        self._panel_rect = pygame.Rect(0, panel_y, width, height)
        _surface = pygame.Surface((width, height))
        _surface.fill(HTMLColor.PURPLE)

        font = pygame.font.Font(None, 25)
        x = 10
        y = 10
        max_per_row = max(1, width // 120)
        entities = self._entity_types["ant"] + self._entity_types["tile"]
        self._panel_buttons.clear()
        for idx, ent_type in enumerate(entities):
            btn_rect = pygame.Rect(x, y + panel_y, 100, 40)
            self._panel_buttons.append(btn_rect.copy())
            pygame.draw.rect(_surface, HTMLColor.WHITE, pygame.Rect(x, y, 100, 40))
            txt = font.render(ent_type, True, HTMLColor.BLACK)
            _surface.blit(txt, (x + 10, y + 10))
            x += 120
            if (idx + 1) % max_per_row == 0:
                x = 10
                y += 50

        self.surface.blit(_surface, (0, panel_y))

    def _handle_panel_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for idx, rect in enumerate(self._panel_buttons):
                if rect.collidepoint(mouse_pos):
                    entities = self._entity_types["ant"] + self._entity_types["tile"]
                    if idx < len(entities):
                        self.selected_entity = entities[idx]
                        self._is_ant_panel_active = False
                    break

    def _render_buttons(self):
        self._save_button.rect.topleft = (10, 10)
        self._load_button.rect.topleft = (10, 70)
        self._save_button.render(self.surface)
        self._load_button.render(self.surface)

    def _save_map(self):
        ants_data = [
            {
                "type": ant.__class__.__name__,
                "position": [int(ant.position[0]), int(ant.position[1])],
            }
            for ant in self.parent.world.ants
        ]
        tiles_data = []
        for y, row in enumerate(self.parent.world.tiles):
            for x, tile in enumerate(row):
                tiles_data.append({
                    "type": tile.__class__.__name__,
                    "position": [x, y],
                })
        data = {"ants": ants_data, "tiles": tiles_data}
        path = os.path.join(os.getcwd(), "data", "world_map.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.parent._menu = False
        self.parent.world.load(data)

    def _load_map(self):
        path = os.path.join(os.getcwd(), "data", "world_map.json")
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            data = json.load(f)
        self.parent.world.load(data)
