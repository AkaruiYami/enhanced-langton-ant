from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame
from common import Alignment
from common.constant import HTMLColor
from common.math import Vector2
from core.world import World
from gui.component import Button
from gui.layout import Column, Row

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

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.surface.fill(HTMLColor.WHITE)

        self._render_grid_lines()

        if self._is_ant_panel_active:
            self._render_selection_panel()

        surface.blit(self.surface, position)

    def update(self, event: pygame.event.EventType):
        if event.type == pygame.MOUSEBUTTONDOWN:
            coor = pygame.mouse.get_pos()
            grid = World.point_to_grid(coor)
            print(f"Mouse click at: {grid} -> {coor}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._is_ant_panel_active = not self._is_ant_panel_active
                _status = "actived" if self._is_ant_panel_active else "deactivated"
                print(f"Ant panel is {_status}")

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

    def _render_selection_panel(self):
        _size = self.surface.get_size()
        height = _size[1] // 4
        width = _size[0]

        _surface = pygame.Surface((width, height))
        _surface.fill(HTMLColor.PURPLE)

        self.surface.blit(_surface, (0, _size[1] - height))
