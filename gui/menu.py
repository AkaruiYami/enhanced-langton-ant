from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame
from common import Alignment
from common.constant import HTMLColor
from common.math import Vector2
from gui.component import Button, TextInput
from gui.layout import Column, Row
import json
import os

from core.registry import AntRegistry, TileRegistry
from gui.dialog import LoadDialog

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
        self._load_dialog = LoadDialog(parent.screen.get_size())

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
        if self._load_dialog.active:
            self._load_dialog.render(surface)

    def update(self, event):
        if self._load_dialog.active:
            self._load_dialog.handle_event(event, on_load=self._do_load)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._load_button.rect.collidepoint(event.pos):
                self._load_dialog.open()
                return
        self.surface.update(event)

    def _do_load(self, filename: str):
        path = os.path.join(os.getcwd(), "data", f"{filename}.json")
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            data = json.load(f)
        self.parent.world.load(data)
        self.parent._menu = False


class EditorMenu(Menu):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.surface = pygame.Surface(parent.screen.get_size())
        self._is_ant_panel_active = False
        self.selected_entity = None
        self._entity_types = self._load_entity_types()
        self._save_button = _construct_button("Save")
        self._load_button = _construct_button("Load")
        self._run_button = _construct_button("Run")
        self._exit_button = _construct_button("Exit")
        self._panel_buttons: list[pygame.Rect] = []
        self._dialog_mode: str | None = None
        self._text_input: TextInput | None = None
        self._load_dialog = LoadDialog(parent.screen.get_size())
        self._pending_save_name: str = ""
        self._confirm_yes: pygame.Rect | None = None
        self._confirm_no: pygame.Rect | None = None
        self._dialog_font = pygame.font.Font(None, 25)
        self._show_buttons = False
        self._cam_x: float = 0.0
        self._cam_y: float = 0.0
        self._zoom: float = 1.0
        self._panning: bool = False
        self._pan_start: tuple[int, int] | None = None

    def _load_entity_types(self):
        from core.registry import AntRegistry, TileRegistry

        return {
            "ant": AntRegistry.names(),
            "tile": TileRegistry.names(),
        }

    def _world_to_screen(self, grid_x: float, grid_y: float) -> tuple[float, float]:
        cell_size = self.parent.conf.tile_config.resolution
        sx = (grid_x * cell_size + self._cam_x) * self._zoom
        sy = (grid_y * cell_size + self._cam_y) * self._zoom
        return sx, sy

    def _screen_to_world(self, screen_x: float, screen_y: float) -> Vector2:
        cell_size = self.parent.conf.tile_config.resolution
        wx = screen_x / self._zoom - self._cam_x
        wy = screen_y / self._zoom - self._cam_y
        gx = int(wx / cell_size)
        gy = int(wy / cell_size)
        return Vector2(gx, gy)

    def render(self, surface: pygame.Surface, position=(0, 0)):
        self.surface.fill(HTMLColor.WHITE)
        self._render_entities()
        self._render_grid_lines()
        self._render_ghost()
        if self._is_ant_panel_active:
            self._render_selection_panel()
        if self._show_buttons:
            self._render_buttons()
        self._render_keybind_tips()
        self._render_selected_element()
        if self._dialog_mode is not None:
            self._render_dialog()
        self._load_dialog.render(self.surface)
        surface.blit(self.surface, position)

    def update(self, event: pygame.event.EventType):
        if self._load_dialog.active:
            self._load_dialog.handle_event(event, on_load=self._do_load)
            return
        if self._dialog_mode is not None:
            self._handle_dialog_event(event)
            return
        if self._is_ant_panel_active:
            self._handle_panel_event(event)
            return
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            old_zoom = self._zoom
            self._zoom *= 1.1 if event.y > 0 else 1 / 1.1
            self._zoom = max(0.2, min(5.0, self._zoom))
            self._cam_x = mx * (1 - self._zoom / old_zoom) + self._cam_x * (self._zoom / old_zoom)
            self._cam_y = my * (1 - self._zoom / old_zoom) + self._cam_y * (self._zoom / old_zoom)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            coor = pygame.mouse.get_pos()
            if event.button == 2:
                self._panning = True
                self._pan_start = coor
                return
            grid = self._screen_to_world(*coor)
            if self._show_buttons:
                if self._save_button.rect.collidepoint(coor):
                    self._open_save_dialog()
                    return
                if self._load_button.rect.collidepoint(coor):
                    self._load_dialog.open()
                    return
                if self._run_button.rect.collidepoint(coor):
                    self._run_simulation()
                    return
                if self._exit_button.rect.collidepoint(coor):
                    self._exit_to_menu()
                    return
            if event.button == 3:
                self._remove_entity_at(grid)
            elif event.button == 1 and self.selected_entity:
                self._place_entity(grid)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                self._panning = False
                self._pan_start = None
                return
        elif event.type == pygame.MOUSEMOTION:
            if self._panning and self._pan_start is not None:
                coor = pygame.mouse.get_pos()
                dx = coor[0] - self._pan_start[0]
                dy = coor[1] - self._pan_start[1]
                self._cam_x += dx / self._zoom
                self._cam_y += dy / self._zoom
                self._pan_start = coor
                return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._is_ant_panel_active = not self._is_ant_panel_active
            elif event.key == pygame.K_ESCAPE:
                self.selected_entity = None
                self._show_buttons = not self._show_buttons

    def _place_entity(self, grid):
        gx, gy = int(grid.x), int(grid.y)
        if self.selected_entity in self._entity_types["ant"]:
            ant = AntRegistry.get(self.selected_entity)
            self.parent.world.ants.append(ant(grid))
        elif self.selected_entity in self._entity_types["tile"]:
            tile = TileRegistry.get(self.selected_entity)
            self.parent.world.tiles[gy][gx] = tile()

    def _remove_entity_at(self, grid):
        gx, gy = int(grid.x), int(grid.y)
        self.parent.world.ants = [
            a for a in self.parent.world.ants
            if int(a.position[0]) != gx or int(a.position[1]) != gy
        ]
        tiles = self.parent.world.tiles
        if 0 <= gy < len(tiles) and 0 <= gx < len(tiles[0]):
            tiles[gy][gx] = TileRegistry.at(0)[1]()

    def _render_grid_lines(self):
        grid_w, grid_h = self.parent.conf.grid_size
        cell_size = self.parent.conf.tile_config.resolution
        screen_w, screen_h = self.surface.get_size()
        for x in range(grid_w + 1):
            sx, _ = self._world_to_screen(x, 0)
            sx = int(sx)
            if sx < 0 or sx > screen_w:
                continue
            pygame.draw.line(self.surface, HTMLColor.BLACK, (sx, 0), (sx, screen_h))
        for y in range(grid_h + 1):
            _, sy = self._world_to_screen(0, y)
            sy = int(sy)
            if sy < 0 or sy > screen_h:
                continue
            pygame.draw.line(self.surface, HTMLColor.BLACK, (0, sy), (screen_w, sy))

    def _render_ghost(self):
        if self.selected_entity is None or self._is_ant_panel_active:
            return
        coor = pygame.mouse.get_pos()
        cell_size = self.parent.conf.tile_config.resolution
        grid = self._screen_to_world(*coor)
        gx, gy = grid.x, grid.y
        grid_w = self.parent.conf.grid_size[0]
        grid_h = self.parent.conf.grid_size[1]
        if gx < 0 or gx >= grid_w or gy < 0 or gy >= grid_h:
            return
        size = max(1, int(cell_size * self._zoom))
        ghost = pygame.Surface((size, size), pygame.SRCALPHA)
        entity_cls = None
        if self.selected_entity in self._entity_types["ant"]:
            entity_cls = AntRegistry.get(self.selected_entity)
        elif self.selected_entity in self._entity_types["tile"]:
            entity_cls = TileRegistry.get(self.selected_entity)
        if entity_cls is None:
            return
        if self.selected_entity in self._entity_types["ant"]:
            color = entity_cls(Vector2(0, 0)).color
        else:
            color = entity_cls().color
        alpha_color = pygame.Color(color.r, color.g, color.b, 128)
        if self.selected_entity in self._entity_types["ant"]:
            pygame.draw.circle(ghost, alpha_color, (size // 2, size // 2), size // 2)
        else:
            pygame.draw.rect(ghost, alpha_color, (0, 0, size, size))
        sx, sy = self._world_to_screen(gx, gy)
        self.surface.blit(ghost, (int(sx), int(sy)))

    def _render_entities(self):
        cell_size = self.parent.conf.tile_config.resolution
        screen_w, screen_h = self.surface.get_size()
        tiles = self.parent.world.tiles
        grid_h = len(tiles)
        grid_w = len(tiles[0]) if grid_h > 0 else 0
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                sx, sy = self._world_to_screen(x, y)
                size = cell_size * self._zoom
                if sx + size < 0 or sx > screen_w or sy + size < 0 or sy > screen_h:
                    continue
                rect = pygame.Rect(int(sx), int(sy), int(size), int(size))
                pygame.draw.rect(self.surface, tile.color, rect)

        for ant in self.parent.world.ants:
            ax, ay = ant.position
            sx, sy = self._world_to_screen(ax + 0.5, ay + 0.5)
            radius = int(cell_size * self._zoom / 2)
            if sx + radius < 0 or sx - radius > screen_w or sy + radius < 0 or sy - radius > screen_h:
                continue
            pygame.draw.circle(self.surface, ant.color, (int(sx), int(sy)), radius)

    def _render_selection_panel(self):
        _size = self.surface.get_size()
        height = _size[1] // 4
        width = _size[0]
        panel_y = _size[1] - height

        _surface = pygame.Surface((width, height))
        _surface.fill(HTMLColor.PURPLE)

        font = pygame.font.Font(None, 25)
        x = 10
        y = 10
        max_per_row = max(1, width // 120)
        entities = self._entity_types["ant"] + self._entity_types["tile"]
        self._panel_buttons.clear()
        for idx, ent_type in enumerate(entities):
            btn_rect = pygame.Rect(x, y + panel_y, 100, 40)
            self._panel_buttons.append(btn_rect.copy())
            pygame.draw.rect(_surface, HTMLColor.WHITE, pygame.Rect(x, y, 100, 40))
            txt = font.render(ent_type, True, HTMLColor.BLACK)
            _surface.blit(txt, (x + 10, y + 10))
            x += 120
            if (idx + 1) % max_per_row == 0:
                x = 10
                y += 50

        self.surface.blit(_surface, (0, panel_y))

    def _handle_panel_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for idx, rect in enumerate(self._panel_buttons):
                if rect.collidepoint(mouse_pos):
                    entities = self._entity_types["ant"] + self._entity_types["tile"]
                    if idx < len(entities):
                        self.selected_entity = entities[idx]
                        self._is_ant_panel_active = False
                    break

    def _get_save_data(self) -> dict:
        ants_data = [
            {
                "type": ant.__class__.__name__,
                "position": [int(ant.position[0]), int(ant.position[1])],
            }
            for ant in self.parent.world.ants
        ]
        tiles_data = []
        for y, row in enumerate(self.parent.world.tiles):
            for x, tile in enumerate(row):
                tiles_data.append({
                    "type": tile.__class__.__name__,
                    "position": [x, y],
                })
        return {"ants": ants_data, "tiles": tiles_data}

    def _open_save_dialog(self):
        self._dialog_mode = "save"
        screen_w, screen_h = self.parent.screen.get_size()
        input_rect = pygame.Rect(screen_w // 2 - 150, screen_h // 2 - 25, 300, 40)
        self._text_input = TextInput(
            font=self._dialog_font,
            foreground=pygame.Color(HTMLColor.BLACK),
            background=pygame.Color(HTMLColor.WHITE),
            cursor_color=pygame.Color(HTMLColor.PURPLE),
            max_length=30,
            rect=input_rect,
        )

    def _open_confirm_dialog(self, filename: str):
        self._dialog_mode = "confirm"
        self._pending_save_name = filename

    def _close_dialog(self):
        self._dialog_mode = None
        self._text_input = None
        self._pending_save_name = ""

    def _do_save(self, filename: str):
        data = self._get_save_data()
        path = os.path.join(os.getcwd(), "data", f"{filename}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.parent._menu = False
        self.parent.world.load(data)

    def _do_load(self, filename: str):
        path = os.path.join(os.getcwd(), "data", f"{filename}.json")
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            data = json.load(f)
        self.parent.world.load(data, running=False)

    def _render_dialog(self):
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.surface.blit(overlay, (0, 0))

        screen_w, screen_h = self.parent.screen.get_size()
        dlg_w, dlg_h = 400, 250
        dlg_rect = pygame.Rect(screen_w // 2 - dlg_w // 2, screen_h // 2 - dlg_h // 2, dlg_w, dlg_h)
        pygame.draw.rect(self.surface, pygame.Color(HTMLColor.PURPLE), dlg_rect)
        pygame.draw.rect(self.surface, pygame.Color(HTMLColor.WHITE), dlg_rect, 2)

        if self._dialog_mode == "save":
            self._render_save_dialog(dlg_rect)
        elif self._dialog_mode == "confirm":
            self._render_confirm_dialog(dlg_rect)

    def _render_save_dialog(self, dlg_rect: pygame.Rect):
        title = self._dialog_font.render("Save As:", True, pygame.Color(HTMLColor.WHITE))
        self.surface.blit(title, (dlg_rect.x + 20, dlg_rect.y + 15))

        if self._text_input:
            self._text_input.rect.x = dlg_rect.x + 20
            self._text_input.rect.y = dlg_rect.y + 50
            self._text_input.render(self.surface)

        btn_y = dlg_rect.bottom - 55
        save_btn_rect = pygame.Rect(dlg_rect.x + 60, btn_y, 100, 40)
        cancel_btn_rect = pygame.Rect(dlg_rect.x + 200, btn_y, 100, 40)
        self._confirm_yes = save_btn_rect
        self._confirm_no = cancel_btn_rect

        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [(save_btn_rect, "Save"), (cancel_btn_rect, "Cancel")]:
            color = pygame.Color(HTMLColor.VIOLET) if rect.collidepoint(mouse_pos) else pygame.Color(HTMLColor.WHITE)
            pygame.draw.rect(self.surface, color, rect)
            txt = self._dialog_font.render(label, True, pygame.Color(HTMLColor.BLACK))
            self.surface.blit(txt, txt.get_rect(center=rect.center))

    def _render_confirm_dialog(self, dlg_rect: pygame.Rect):
        msg = self._dialog_font.render(f'Overwrite "{self._pending_save_name}"?', True, pygame.Color(HTMLColor.WHITE))
        self.surface.blit(msg, (dlg_rect.x + 20, dlg_rect.y + 30))

        btn_y = dlg_rect.bottom - 55
        yes_btn_rect = pygame.Rect(dlg_rect.x + 80, btn_y, 100, 40)
        no_btn_rect = pygame.Rect(dlg_rect.x + 220, btn_y, 100, 40)
        self._confirm_yes = yes_btn_rect
        self._confirm_no = no_btn_rect

        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [(yes_btn_rect, "Yes"), (no_btn_rect, "No")]:
            color = pygame.Color(HTMLColor.VIOLET) if rect.collidepoint(mouse_pos) else pygame.Color(HTMLColor.WHITE)
            pygame.draw.rect(self.surface, color, rect)
            txt = self._dialog_font.render(label, True, pygame.Color(HTMLColor.BLACK))
            self.surface.blit(txt, txt.get_rect(center=rect.center))

    def _handle_dialog_event(self, event: pygame.event.EventType):
        if self._dialog_mode == "save":
            self._handle_save_dialog_event(event)
        elif self._dialog_mode == "confirm":
            self._handle_confirm_dialog_event(event)

    def _handle_save_dialog_event(self, event: pygame.event.EventType):
        if self._text_input:
            result = self._text_input.handle_event(event)
            if result is not None and result.strip():
                filename = result.strip()
                data_dir = os.path.join(os.getcwd(), "data")
                path = os.path.join(data_dir, f"{filename}.json")
                if os.path.exists(path):
                    self._open_confirm_dialog(filename)
                else:
                    self._do_save(filename)
                    self._close_dialog()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._close_dialog()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._confirm_yes and self._confirm_yes.collidepoint(event.pos):
                if self._text_input:
                    filename = self._text_input.get_text().strip()
                    if filename:
                        self._do_save(filename)
                        self._close_dialog()
            if self._confirm_no and self._confirm_no.collidepoint(event.pos):
                self._close_dialog()

    def _handle_confirm_dialog_event(self, event: pygame.event.EventType):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._confirm_yes and self._confirm_yes.collidepoint(event.pos):
                self._do_save(self._pending_save_name)
                self._close_dialog()
            if self._confirm_no and self._confirm_no.collidepoint(event.pos):
                self._dialog_mode = "save"
                self._pending_save_name = ""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._dialog_mode = "save"
            self._pending_save_name = ""

    def _render_buttons(self):
        self._save_button.rect.topleft = (10, 10)
        self._load_button.rect.topleft = (10, 70)
        self._run_button.rect.topleft = (10, 130)
        self._exit_button.rect.topleft = (10, 190)
        self._save_button.render(self.surface)
        self._load_button.render(self.surface)
        self._run_button.render(self.surface)
        self._exit_button.render(self.surface)

    def _render_keybind_tips(self):
        font = pygame.font.Font(None, 20)
        tips = "LMB: place  |  RMB: delete  |  Esc: menu  |  A: panel  |  Scroll: zoom  |  MMB: pan"
        text = font.render(tips, True, HTMLColor.WHITE)
        screen_w, screen_h = self.surface.get_size()
        bg_rect = pygame.Rect(0, screen_h - 28, screen_w, 28)
        bg = pygame.Surface((screen_w, 28), pygame.SRCALPHA)
        bg.fill(pygame.Color(0, 0, 0, 160))
        self.surface.blit(bg, bg_rect)
        text_rect = text.get_rect(center=(screen_w // 2, screen_h - 14))
        self.surface.blit(text, text_rect)

    def _render_selected_element(self):
        if self.selected_entity is None:
            return
        font = pygame.font.Font(None, 22)
        text = font.render(f"Selected: {self.selected_entity}", True, HTMLColor.WHITE)
        screen_w, _ = self.surface.get_size()
        text_rect = text.get_rect(topright=(screen_w - 10, 10))
        bg_rect = text_rect.inflate(12, 6)
        bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg.fill(pygame.Color(0, 0, 0, 160))
        self.surface.blit(bg, bg_rect)
        self.surface.blit(text, text_rect)

    def _run_simulation(self):
        self.parent._menu = False
        self.parent.world.running = True

    def _exit_to_menu(self):
        self.parent.p = FrontMenu(self.parent)
