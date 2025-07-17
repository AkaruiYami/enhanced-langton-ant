import pygame
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

    def _construct_menu(self):
        row = Row()
        column = Column()
        column.push(_construct_button("New"))
        column.push(_construct_button("Load"))
        column.push(_construct_button("Quit"))
        row.push(column)
        return row

    def render(self, surface: pygame.Surface, position=(0, 0)):
        surf = self._construct_menu()
        surf.render(surface, position)

    def update(self, event):
        pass


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
        if self.pause_button.is_clicked(event):
            print("Button Clicked!")
