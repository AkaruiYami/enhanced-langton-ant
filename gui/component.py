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


class TextInput(Component):
    def __init__(
        self,
        font: pygame.font.Font,
        foreground: pygame.Color,
        background: pygame.Color,
        cursor_color: pygame.Color,
        max_length: int = 30,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.font = font
        self.foreground = foreground
        self.background = background
        self.cursor_color = cursor_color
        self.max_length = max_length
        self.text = ""
        self.active = True
        self._cursor_timer = 0
        self._cursor_visible = True

    def get_text(self):
        return self.text

    def set_text(self, value: str):
        self.text = value[:self.max_length]

    def clear(self):
        self.text = ""

    def handle_event(self, event: pygame.event.EventType) -> str | None:
        if not self.active:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode and event.unicode.isprintable():
                if len(self.text) < self.max_length:
                    self.text += event.unicode
        return None

    def render(self, surface: pygame.Surface, position=(0, 0)):
        pygame.draw.rect(surface, self.background, self.rect)
        pygame.draw.rect(surface, self.cursor_color, self.rect, 2)

        display_text = self.text
        text_surf = self.font.render(display_text, True, self.foreground)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 8, self.rect.centery))
        surface.blit(text_surf, text_rect)

        if self.active and self._cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_y1 = self.rect.y + 6
            cursor_y2 = self.rect.bottom - 6
            pygame.draw.line(surface, self.cursor_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

    def update(self, event: pygame.event.EventType):
        self._cursor_timer += 1
        if self._cursor_timer >= 30:
            self._cursor_timer = 0
            self._cursor_visible = not self._cursor_visible
