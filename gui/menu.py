import pygame
from common import Alignment
from common import constant
from common.constant import HTMLColor
from gui.component import Button
from gui.layout import Column, Row


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


class FrontMenu:
    def __init__(self, parent):
        self.parent = parent
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
        bg.fill(constant.HTMLColor.BLACK + "80")

        surface.blit(bg, (0, 0))
        self.surface.render(surface, position)

    def update(self, event):
        self.surface.update(event)


class PauseMenu:
    def __init__(self, size):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.pause_button = Button(
            "Pause",
            pygame.Color(HTMLColor.WHITE),
            pygame.Color(HTMLColor.PURPLE),
            pygame.Color(HTMLColor.VIOLET),
            pygame.font.Font(None, 25),
            True,
            rect=pygame.Rect(0, 0, 200, 50),
        )
        self.disable = False

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.pause_button.render(self.surface)
        surface.blit(self.surface, (0, 0))

    def update(self, event):
        pass
