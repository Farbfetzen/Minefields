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
