import pygame
from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface, position=(0, 0)): ...


class Button(Component):
    def __init__(
        self,
        label: str,
        rect: pygame.Rect,
        foreground: pygame.Color,
        background: pygame.Color,
        highlight: pygame.Color,
        font: pygame.font.Font,
        antialias: bool,
    ):
        self.label = label
        self.rect = rect
        self.foreground = foreground
        self.background = background
        self.highlight = highlight
        self.font = font
        self.antialias = antialias

    def render(self, surface: pygame.Surface, position=(0, 0)):
        adjusted_rect = self.rect.move(position)
        self._draw_rect(surface, adjusted_rect)
        self._draw_text(surface, adjusted_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def _draw_rect(self, surface, rect):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.highlight if is_hovered else self.background
        pygame.draw.rect(surface, color, rect)

    def _draw_text(self, surface, rect):
        text = self.font.render(self.label, self.antialias, self.foreground)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
