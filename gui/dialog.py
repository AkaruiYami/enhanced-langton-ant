from typing import Callable
import os
import pygame
from common.constant import HTMLColor
from common.paths import get_data_dir


class LoadDialog:
    def __init__(self, screen_size: tuple[int, int]):
        self._screen_size = screen_size
        self._font = pygame.font.Font(None, 25)
        self._file_list: list[str] = []
        self._file_buttons: list[pygame.Rect] = []
        self._cancel_btn: pygame.Rect | None = None
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    def open(self):
        self._active = True
        self._file_list = self._get_saved_files()
        self._file_buttons.clear()

    def close(self):
        self._active = False
        self._file_list.clear()
        self._file_buttons.clear()

    def _get_saved_files(self) -> list[str]:
        data_dir = get_data_dir()
        if not data_dir.exists():
            return []
        return sorted(
            f[:-5] for f in os.listdir(data_dir)
            if f.endswith(".json")
        )

    def render(self, surface: pygame.Surface):
        if not self._active:
            return

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        screen_w, screen_h = self._screen_size
        dlg_w, dlg_h = 400, 250
        dlg_rect = pygame.Rect(
            screen_w // 2 - dlg_w // 2,
            screen_h // 2 - dlg_h // 2,
            dlg_w,
            dlg_h,
        )
        pygame.draw.rect(surface, pygame.Color(HTMLColor.PURPLE), dlg_rect)
        pygame.draw.rect(surface, pygame.Color(HTMLColor.WHITE), dlg_rect, 2)

        title = self._font.render("Load World:", True, pygame.Color(HTMLColor.WHITE))
        surface.blit(title, (dlg_rect.x + 20, dlg_rect.y + 15))

        self._file_buttons.clear()
        if not self._file_list:
            empty = self._font.render(
                "No saved files found", True, pygame.Color(HTMLColor.WHITE)
            )
            surface.blit(empty, (dlg_rect.x + 20, dlg_rect.y + 60))
        else:
            y = dlg_rect.y + 50
            for filename in self._file_list:
                btn_rect = pygame.Rect(dlg_rect.x + 20, y, dlg_rect.w - 40, 35)
                self._file_buttons.append(btn_rect)
                mouse_pos = pygame.mouse.get_pos()
                color = (
                    pygame.Color(HTMLColor.VIOLET)
                    if btn_rect.collidepoint(mouse_pos)
                    else pygame.Color(HTMLColor.WHITE)
                )
                pygame.draw.rect(surface, color, btn_rect)
                txt = self._font.render(filename, True, pygame.Color(HTMLColor.BLACK))
                surface.blit(txt, (btn_rect.x + 10, btn_rect.y + 8))
                y += 42

        cancel_y = dlg_rect.bottom - 55
        cancel_btn_rect = pygame.Rect(dlg_rect.x + 140, cancel_y, 120, 40)
        self._cancel_btn = cancel_btn_rect
        mouse_pos = pygame.mouse.get_pos()
        color = (
            pygame.Color(HTMLColor.VIOLET)
            if cancel_btn_rect.collidepoint(mouse_pos)
            else pygame.Color(HTMLColor.WHITE)
        )
        pygame.draw.rect(surface, color, cancel_btn_rect)
        txt = self._font.render("Cancel", True, pygame.Color(HTMLColor.BLACK))
        surface.blit(txt, txt.get_rect(center=cancel_btn_rect.center))

    def handle_event(
        self, event: pygame.event.EventType, on_load: Callable[[str], None]
    ) -> bool:
        if not self._active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self._file_buttons):
                if rect.collidepoint(event.pos) and idx < len(self._file_list):
                    on_load(self._file_list[idx])
                    self.close()
                    return True
            if self._cancel_btn and self._cancel_btn.collidepoint(event.pos):
                self.close()
                return True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
            return True

        return True
