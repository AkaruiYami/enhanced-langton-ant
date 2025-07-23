from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame
from common import Alignment
from common.constant import HTMLColor
from common.math import Vector2
from core.ant import Ant
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
        self.ants: list[Ant] = []
        self.tiles = {}
        self._entity_types = self._load_entity_types()
        self._save_button = _construct_button("Save")
        self._load_button = _construct_button("Load")

    def _load_entity_types(self):
        from core.registry import AntRegistry, TileRegistry

        return {
            "ant": AntRegistry.names(),
            "tile": TileRegistry.names(),
        }

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.surface.fill(HTMLColor.WHITE)
        self._render_grid_lines()
        self._render_entities()
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
            grid = World.point_to_grid(coor)
            # Check Save/Load button clicks
            if self._save_button.rect.collidepoint(coor):
                self._save_map()
                print("Map saved.")
                return
            if self._load_button.rect.collidepoint(coor):
                self._load_map()
                print("Map loaded.")
                return
            if self.selected_entity:
                self._place_entity(grid)
            print(f"Mouse click at: {grid} -> {coor}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._is_ant_panel_active = not self._is_ant_panel_active
                _status = "actived" if self._is_ant_panel_active else "deactivated"
                print(f"Ant panel is {_status}")

    def _place_entity(self, grid):
        if self.selected_entity in self._entity_types["ant"]:
            ant = AntRegistry.get(self.selected_entity)
            self.ants.append(ant(grid))
        elif self.selected_entity in self._entity_types["tile"]:
            tile = TileRegistry.get(self.selected_entity)
            self.tiles[tuple(grid)] = tile()

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

    def _render_entities(self):
        cell_size = self.parent.conf.tile_config.resolution
        for grid, tile in self.tiles.items():
            x, y = grid
            rect = pygame.Rect(
                x * cell_size,
                y * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(self.surface, tile.color, rect)

        for ant in self.ants:
            ax, ay = ant.position
            center_x = ax * cell_size + cell_size // 2
            center_y = ay * cell_size + cell_size // 2
            radius = cell_size // 2
            pygame.draw.circle(self.surface, ant.color, (center_x, center_y), radius)

    def _render_selection_panel(self):
        _size = self.surface.get_size()
        height = _size[1] // 4
        width = _size[0]

        _surface = pygame.Surface((width, height))
        _surface.fill(HTMLColor.PURPLE)

        # TODO: properly draw the entity type buttons
        font = pygame.font.Font(None, 25)
        x = 10
        y = 10
        max_per_row = max(1, width // 120)
        entities = self._entity_types["ant"] + self._entity_types["tile"]
        for idx, ent_type in enumerate(entities):
            btn_rect = pygame.Rect(x, y, 100, 40)
            pygame.draw.rect(_surface, HTMLColor.WHITE, btn_rect)
            txt = font.render(ent_type, True, HTMLColor.BLACK)
            _surface.blit(txt, (x + 10, y + 10))
            x += 120
            if (idx + 1) % max_per_row == 0:
                x = 10
                y += 50

        self.surface.blit(_surface, (0, _size[1] - height))

    def _handle_panel_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            panel_top = self.surface.get_size()[1] - self.surface.get_size()[1] // 4
            if mouse_y >= panel_top:
                rel_x = mouse_x - 10
                rel_y = mouse_y - panel_top + 10
                max_per_row = max(1, self.surface.get_size()[0] // 120)
                col = rel_x // 120
                row = rel_y // 50
                idx = row * max_per_row + col
                entities = self._entity_types["ant"] + self._entity_types["tile"]
                if 0 <= idx < len(entities):
                    self.selected_entity = entities[idx]
                    print(f"Selected entity: {self.selected_entity}")
                    self._is_ant_panel_active = False

    def _render_buttons(self):
        self._save_button.rect.topleft = (10, 10)
        self._load_button.rect.topleft = (10, 70)
        self._save_button.render(self.surface)
        self._load_button.render(self.surface)

    def _save_map(self):
        # TODO: ask user what name should it use to save the map
        ants_data = [
            {
                "type": ant.__class__.__name__,
                "position": [int(ant.position[0]), int(ant.position[1])],
            }
            for ant in self.ants
        ]
        tiles_data = [
            {"type": tile.__class__.__name__, "position": [int(pos[0]), int(pos[1])]}
            for pos, tile in self.tiles.items()
        ]
        data = {"ants": ants_data, "tiles": tiles_data}
        path = os.path.join(os.getcwd(), "data/world_map.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.parent._menu = False
        self.parent.world.load(data)

    def _load_map(self):
        pass
