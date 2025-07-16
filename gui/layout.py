from typing import Optional
import pygame
from gui.component import Component

# TODO: abstarct the {Row | Column}._compute_size method


class Layout:
    def __init__(
        self,
        items: Optional[list[Component]] = None,
        rect: Optional[pygame.Rect] = None,
        padding: Optional[int] = None,
    ):
        self.items = _gather_components(items)
        if padding is None:
            padding = 0
        self.padding = padding
        self.rect = rect

    def _render_items(
        self,
        surface: pygame.Surface,
        position: tuple[int, int],
        item_size: tuple[int, int],
        horizontal: bool = True,
    ):
        x, y = position
        for item in self.items:
            rect = pygame.Rect(x, y, item_size[0], item_size[1])
            item.render(surface, rect)

            if horizontal:
                x += item_size[0] + self.padding
            else:
                y += item_size[1] + self.padding


def _gather_components(items) -> list[Component]:
    components = []
    for item in items:
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        components.append(item)
    return components


class Row(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compute_size(self, surface: pygame.Surface):
        item_count = len(self.items)
        alloc_x, alloc_y = surface.get_size()
        alloc_x -= int(self.padding * (item_count - 1))
        new_x = alloc_x // item_count
        return new_x, alloc_y

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)

    def render(self, surface: pygame.Surface, position=(0, 0)):
        if self.rect:
            row_surface = pygame.Surface(self.rect.size, flags=surface.get_flags())
            width, height = self._compute_size(row_surface)
            self._render_items(row_surface, position, (width, height))
            surface.blit(row_surface, self.rect.topleft)
        else:
            width, height = self._compute_size(surface)
            self._render_items(surface, position, (width, height))


class Column(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compute_size(self, surface: pygame.Surface):
        item_count = len(self.items)
        alloc_x, alloc_y = surface.get_size()
        alloc_y -= int(self.padding * (item_count - 1))
        new_y = alloc_y // item_count
        return alloc_x, new_y

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)

    def render(self, surface: pygame.Surface, position=(0, 0)):
        if self.rect:
            row_surface = pygame.Surface(self.rect.size, flags=surface.get_flags())
            width, height = self._compute_size(row_surface)
            self._render_items(row_surface, position, (width, height), False)
            surface.blit(row_surface, self.rect.topleft)
        else:
            width, height = self._compute_size(surface)
            self._render_items(surface, position, (width, height), False)


# TODO: implement grid layout
class Grid(Layout):
    pass
