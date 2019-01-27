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


import os

import pygame as pg


STANDARD_WINDOW_SIZE = (400, 300)
FPS_MAX = 60
START_STATE_NAME = "SplashScreen"
COLORS = {"background_color": (170, 185, 215),
          "font": (200, 200, 200),
          1: (0, 170, 225),
          2: (0, 186, 101),
          3: (223, 138, 0),
          4: (207, 0, 239),
          5: (0, 117, 207),
          6: (0, 138, 0),
          7: (239, 85, 32),
          8: (117, 0, 255),
          "?": (170, 0, 0)}
BOX_TILE_NAMES = ("topleft", "top", "topright",
                  "left", "center", "right",
                  "bottomleft", "bottom", "bottomright")
BUTTON_SIZE = (100, 35)
BIG_BUTTON_SIZE = (150, 50)
RESOURCES_DIR = os.path.join("..", "resources")


# Initialize pygame and the display:
os.environ["SDL_VIDEO_CENTERED"] = "1"
pg.init()
# The icon should be 4 bit (16 colors) and size 32x32 without anti-aliasing.
# To prevent distortion, create a 16x16 icon, then resize it to 32x32
# without anti-aliasing and save it with 4bpp. Then load the 32x32 icon
# here (it will get resized to 16x16):
icon = pg.image.load(os.path.join(RESOURCES_DIR, "icon.png"))
pg.display.set_icon(icon)
pg.display.set_caption("Minefields")
display_surface = pg.display.set_mode(STANDARD_WINDOW_SIZE)


# Fonts are down here because they need pg.init() to be called first.
FONT = os.path.join(RESOURCES_DIR, "freesansbold.ttf")
SMALL_FONT = pg.font.Font(FONT, 15)
MEDIUM_FONT = pg.font.Font(FONT, 20)
BIG_FONT = pg.font.Font(FONT, 30)


# Load and display the splashscreen:
SPLASHSCREEN_IMAGE = pg.image.load(os.path.join(RESOURCES_DIR,
                                                "splashscreen.png")).convert()
display_surface.blit(SPLASHSCREEN_IMAGE, (0, 0))
pg.display.update()


def cut_sheet(sheet, tile_width, tile_height):
    sheet_width, sheet_height = sheet.get_size()
    cols = sheet_width // tile_width
    rows = sheet_height // tile_height
    images = []
    for r in range(rows):
        for c in range(cols):
            image = pg.Surface((tile_width, tile_height)).convert()
            image.blit(sheet, (0, 0), (c*tile_width, r*tile_height,
                                       tile_width, tile_height))
            images.append(image)
    return images


def load_tiles(sheet):
    tile_width, tile_height = (i//3 for i in sheet.get_size())
    images = cut_sheet(sheet, tile_width, tile_height)
    tiles = dict(zip(BOX_TILE_NAMES, images))
    tiles["width"] = tile_width
    tiles["height"] = tile_height
    return tiles


# Load the minefield spritesheet, cut it up into separate resources and store
# them in a dict:
MINEFIELD_TILE_SIZE = 21
minefield_spritesheet = pg.image.load(os.path.join(RESOURCES_DIR,
                                      "minefield.png")).convert()
minefield_tile_images = cut_sheet(minefield_spritesheet, MINEFIELD_TILE_SIZE,
                                  MINEFIELD_TILE_SIZE)
minefield_tile_names = (0, "covered", "covered_highlighted", "mine_exploded",
                        "mine", "flag", "flag_highlighted", "flag_wrong")
minefield_tiles = dict(zip(minefield_tile_names, minefield_tile_images))


# create the numbered tiles:
tile_font = pg.font.Font(None, 25)
for i in range(1, 9):
    num = tile_font.render(str(i), True, COLORS[i])
    num_rect = num.get_rect(center=(10, 12))
    tile = minefield_tile_images[0].copy()
    tile.blit(num, num_rect)
    minefield_tiles[i] = tile


# create the "?" tile:
questionmark = tile_font.render("?", True, COLORS["?"])
q_tile_covered = minefield_tile_images[1].copy()
q_tile_covered.blit(questionmark, questionmark.get_rect(center=(10, 12)))
q_tile_highlight = minefield_tile_images[2].copy()
q_tile_highlight.blit(questionmark, questionmark.get_rect(center=(10, 12)))
minefield_tiles["questionmark"] = q_tile_covered
minefield_tiles["questionmark_highlighted"] = q_tile_highlight


# load the other spritesheets:
box_spritesheet = pg.image.load(os.path.join(RESOURCES_DIR,
                                             "box.png")).convert()
box_tiles = load_tiles(box_spritesheet)
textbox_spritesheet = pg.image.load(os.path.join(RESOURCES_DIR,
                                                 "textbox.png")).convert()
textbox_tiles = load_tiles(textbox_spritesheet)
button_idle_spritesheet = pg.image.load(
    os.path.join(RESOURCES_DIR, "button_idle.png")).convert()
button_idle_tiles = load_tiles(button_idle_spritesheet)
button_active_spritesheet = pg.image.load(
    os.path.join(RESOURCES_DIR, "button_active.png")).convert()
button_active_tiles = load_tiles(button_active_spritesheet)
button_locked_spritesheet = pg.image.load(
    os.path.join(RESOURCES_DIR, "button_locked.png")).convert()
button_locked_tiles = load_tiles(button_locked_spritesheet)
