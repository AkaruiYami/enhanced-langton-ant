import pygame
from abc import ABC, abstractmethod
from common.event import UI_BUTTON_CLICKED


class Component(ABC):
    def __init__(
        self,
        rect: pygame.Rect,
        expand_x: bool = False,
        expand_y: bool = False,
    ):
        self.rect = rect
        self._expand_x = expand_x
        self._expand_y = expand_y

    @abstractmethod
    def render(self, surface: pygame.Surface, position: tuple[int, int] = (0, 0)): ...

    @abstractmethod
    def update(self, event: pygame.event.EventType): ...

    def get_rect(self):
        return self.rect.copy()


class Button(Component):
    def __init__(
        self,
        label: str,
        foreground: pygame.Color,
        background: pygame.Color,
        highlight: pygame.Color,
        font: pygame.font.Font,
        antialias: bool,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.label = label
        self.foreground = foreground
        self.background = background
        self.highlight = highlight
        self.font = font
        self.antialias = antialias

    def render(self, surface: pygame.Surface, position=(0, 0)):
        if self.rect is None:
            raise ValueError
        self._draw_rect(surface, self.rect)
        self._draw_text(surface, self.rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                _event = pygame.event.Event(UI_BUTTON_CLICKED, {"buttonId": self.label})
                pygame.event.post(_event)

    def _draw_rect(self, surface, rect):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = self.highlight if is_hovered else self.background
        pygame.draw.rect(surface, color, rect)

    def _draw_text(self, surface, rect):
        text = self.font.render(self.label, self.antialias, self.foreground)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
