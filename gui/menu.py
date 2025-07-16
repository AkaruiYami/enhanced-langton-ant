import pygame
from common.constant import HTMLColor
from gui.component import Button


class FrontMenu:
    def __init__(self, parent):
        self.parent = parent

    def _construct_button(self):
        pass

    def render(self, surface: pygame.Surface):
        pass

    def update(self, event):
        pass


class PauseMenu:
    def __init__(self, size):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.pause_button = Button(
            "Pause",
            pygame.Rect(0, 0, 200, 50),
            pygame.Color(HTMLColor.WHITE),
            pygame.Color(HTMLColor.PURPLE),
            pygame.Color(HTMLColor.VIOLET),
            pygame.font.Font(None, 25),
            True,
        )
        self.disable = False

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.pause_button.render(self.surface)
        surface.blit(self.surface, (0, 0))

    def update(self, event):
        if self.pause_button.is_clicked(event):
            print("Button Clicked!")
