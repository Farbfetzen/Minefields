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


import pygame as pg

import prepare


class Box:
    def __init__(self, size, pos, text=None, font=prepare.MEDIUM_FONT,
                 tiles=prepare.box_tiles, centerx=False, centery=False,
                 name=None):
        self.tiles = tiles
        self.width, self.height = size
        self.tile_width, self.tile_height = tiles["topleft"].get_rect().size
        self.box_surface = pg.Surface(size).convert()
        self.background = pg.Surface(size).convert()
        x, y = pos
        # centerx and centery center the box on the given pos:
        if centerx:
            x -= size[0] // 2
        if centery:
            y -= size[1] // 2
        self.rect = pg.Rect((x, y), size)
        self.font = font
        if name is not None:
            self.name = name

        for x in range(self.tile_width, self.width - self.tile_width,
                       self.tile_width):
            for y in range(self.tile_height, self.height - self.tile_height,
                           self.tile_height):
                self.background.blit(self.tiles["center"], (x, y))
        for x in range(self.tile_width, self.width - self.tile_width,
                       self.tile_width):
            self.background.blit(tiles["top"], (x, 0))
            self.background.blit(tiles["bottom"],
                                 (x, self.height - self.tile_height))
        for y in range(self.tile_height, self.height - self.tile_height,
                       self.tile_height):
            self.background.blit(tiles["left"], (0, y))
            self.background.blit(tiles["right"],
                                 (self.width - self.tile_width, y))
        self.background.blit(tiles["topleft"], (0, 0))
        self.background.blit(tiles["topright"],
                             (self.width - self.tile_width, 0))
        self.background.blit(tiles["bottomleft"],
                             (0, self.height - self.tile_height))
        self.background.blit(tiles["bottomright"],
                             (self.width - self.tile_width,
                              self.height - self.tile_height))
        self.box_surface.blit(self.background, (0, 0))
        if text is not None:
            self.update(text)

    def update(self, text):
        self.box_surface.blit(self.background, (0, 0))

        text_render = self.font.render(text, True, prepare.COLORS["font"])
        text_rect = text_render.get_rect(center=(self.width//2, self.height//2))
        text_rect.y -= self.font.get_descent() // 2
        self.box_surface.blit(text_render, text_rect)

    def draw(self, surface):
        surface.blit(self.box_surface, self.rect)
