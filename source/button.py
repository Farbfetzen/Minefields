"""Copyright (C) 2019 Sebastian Henz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


import box
import prepare


class Button:
    def __init__(self, pos, text, centerx=True, centery=False,
                 size=prepare.BUTTON_SIZE):
        self.text = text
        if size == prepare.BIG_BUTTON_SIZE:
            font = prepare.BIG_FONT
        else:
            font = prepare.MEDIUM_FONT
        self.idle_surface = box.Box(size, pos, text=self.text, font=font,
                                    tiles=prepare.button_idle_tiles,
                                    centerx=centerx, centery=centery)
        self.active_surface = box.Box(size, pos, text=self.text, font=font,
                                      tiles=prepare.button_active_tiles,
                                      centerx=centerx, centery=centery)
        self.locked_surface = box.Box(size, pos, text=self.text, font=font,
                                      tiles=prepare.button_locked_tiles,
                                      centerx=centerx, centery=centery)
        self.rect = self.idle_surface.rect
        self.active = False
        self.clicked = False
        self.locked = False

    def update(self, mouse_pos, left_click):
        if self.rect.collidepoint(mouse_pos) and not self.locked:
            self.active = True
            if left_click:
                self.clicked = True
        else:
            self.active = False

    def draw(self, surface):
        if self.locked:
            self.locked_surface.draw(surface)
        elif self.active:
            self.active_surface.draw(surface)
        else:
            self.idle_surface.draw(surface)
