from abc import abstractmethod
from typing import Optional
import pygame
from gui.component import Component
from common import Alignment


class Layout(Component):
    def __init__(
        self,
        items: Optional[list[Component]] = None,
        spacing: Optional[int] = None,
        alignment: Alignment = Alignment.START,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.items = []
        self._gather_components(items)
        if spacing is None:
            spacing = 0
        self.spacing = spacing
        self.alignment = alignment

    @abstractmethod
    def push(self, item: Component): ...

    def update(self, event: pygame.event.EventType):
        for item in self.items:
            item.update(event)

    def _gather_components(self, items):
        self.items = []
        if items is None:
            return
        for item in items:
            if not isinstance(item, Component):
                raise TypeError(f"{item} is not a Component type.")
            self.push(item)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


class Row(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)
        self._update_items()

    def _update_items(self):
        extra_spacing = self.spacing * (len(self.items) - 1)
        total_width = sum(item.rect.width for item in self.items) + extra_spacing

        if self.alignment == Alignment.START:
            x_offset = self.rect.left
        elif self.alignment == Alignment.CENTER:
            x_offset = self.rect.left + (self.rect.width - total_width) // 2
        elif self.alignment == Alignment.END:
            x_offset = self.rect.right - total_width
        else:
            raise ValueError(f"Undefined alignment value: {self.alignment}")

        for item in self.items:
            item.rect.topleft = (x_offset, self.rect.top)
            x_offset += item.rect.width + self.spacing

    def render(self, surface: pygame.Surface, position: tuple[int, int] = (0, 0)):
        for item in self.items:
            item.render(surface)


class Column(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def push(self, item: Component):
        if not isinstance(item, Component):
            raise TypeError(f"{item} is not a Component type.")
        self.items.append(item)
        self._update_items()

    def _update_items(self):
        extra_spacing = self.spacing * (len(self.items) - 1)
        total_height = sum(item.rect.height for item in self.items) + extra_spacing

        if self.alignment == Alignment.START:
            y_offset = self.rect.top
        elif self.alignment == Alignment.CENTER:
            y_offset = self.rect.top + (self.rect.height - total_height) // 2
        elif self.alignment == Alignment.END:
            y_offset = self.rect.bottom - total_height
        else:
            raise ValueError(f"Undefined alignment value: {self.alignment}")

        for item in self.items:
            item.rect.topleft = (self.rect.left, y_offset)
            y_offset += item.rect.height + self.spacing

    def render(self, surface: pygame.Surface, position=(0, 0)):
        for item in self.items:
            item.render(surface)


# TODO: implement grid layout
class Grid(Layout):
    pass
