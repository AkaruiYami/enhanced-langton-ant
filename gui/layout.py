from typing import Optional
import pygame
from gui.component import Component
from common import Alignment


# FIXME: makae the layout compact / hugs the items
class Layout(Component):
    def __init__(
        self,
        items: Optional[list[Component]] = None,
        padding: Optional[int] = None,
        alignment: Alignment = Alignment.CENTER,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.items = _gather_components(items)
        if padding is None:
            padding = 0
        self.padding = padding
        self.alignment = alignment

    def _render_items(
        self,
        surface: pygame.Surface,
        position: tuple[int, int],
        item_size: tuple[int, int],
        horizontal: bool = True,
    ):
        x, y = position
        for item in self.items:
            item.render(surface, (x, y))

            if horizontal:
                x += item_size[0] + self.padding
            else:
                y += item_size[1] + self.padding

    def _compute_size(
        self, surface: pygame.Surface, allocate_x=False, allocate_y=False
    ):
        item_count = len(self.items)
        alloc_x, alloc_y = surface.get_size()

        if allocate_x:
            alloc_x -= int(self.padding * (item_count - 1))
            alloc_x = alloc_x // item_count

        if allocate_y:
            alloc_y -= int(self.padding * (item_count - 1))
            alloc_y = alloc_y // item_count

        return alloc_x, alloc_y


def _gather_components(items) -> list[Component]:
    if not items:
        return []

    components = []
    for item in items:
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        components.append(item)
    return components


class Row(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)

    def render(self, surface: pygame.Surface, position=(0, 0)):
        if self.rect:
            row_surface = pygame.Surface(self.rect.size, flags=surface.get_flags())
            width, height = self._compute_size(row_surface, allocate_x=True)
            self._render_items(row_surface, position, (width, height))
            surface.blit(row_surface, self.rect.topleft)
        else:
            width, height = self._compute_size(surface, allocate_x=True)
            self._render_items(surface, position, (width, height))


class Column(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)

    def render(self, surface: pygame.Surface, position=(0, 0)):
        if self.rect:
            row_surface = pygame.Surface(self.rect.size, flags=surface.get_flags())
            width, height = self._compute_size(row_surface, allocate_y=True)
            self._render_items(row_surface, position, (width, height), False)
            surface.blit(row_surface, self.rect.topleft)
        else:
            width, height = self._compute_size(surface, allocate_y=True)
            self._render_items(surface, position, (width, height), False)


# TODO: implement grid layout
class Grid(Layout):
    pass
