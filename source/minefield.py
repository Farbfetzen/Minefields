import random

import pygame as pg

import prepare


class Minefield:
    def __init__(self, width, height, number_of_mines):
        self.width = width
        self.height = height
        self.num_mines = number_of_mines

        self.tiles = prepare.minefield_tiles
        self.tile_size = prepare.MINEFIELD_TILE_SIZE
        self.surface = pg.Surface((width * self.tile_size,
                                   height * self.tile_size)).convert()
        self.pos = (0, 0)  # the pos of the minefield surface in the window
        self.mouseover_tile = None
        self.game_done = False
        self.mines_remaining = self.num_mines
        self.mines_remaining_changed = True
        self.end_message = None

        self.grid = set(((x, y) for x in range(self.width)
                         for y in range(self.height)))
        self.covered = self.grid.copy()
        self.mines = set(random.sample(self.grid, self.num_mines))
        self.neighbors = {}
        for pos in self.grid:
            neighbor_list = []
            for x, y in ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                         (0, 1), (1, -1), (1, 0), (1, 1)):
                neighbor = (pos[0] + x, pos[1] + y)
                if neighbor in self.grid:
                    neighbor_list.append(neighbor)
            self.neighbors[pos] = neighbor_list
        self.hints = {}
        for pos in self.grid:
            if pos not in self.mines:
                hint = 0
                for neighbor in self.neighbors[pos]:
                    if neighbor in self.mines:
                        hint += 1
                self.hints[pos] = hint
        self.flags = set()
        self.questionmarks = set()
        self.exploded_mines = set()
        self.wrong_flags = set()

        self.refresh_surface()

    def refresh_surface(self):
        for pos in self.grid:
            blit_pos = (pos[0] * self.tile_size,
                        pos[1] * self.tile_size)

            if pos in self.covered:
                if pos in self.flags:
                    self.surface.blit(self.tiles["flag"], blit_pos)
                    if pos in self.wrong_flags:
                        self.surface.blit(self.tiles["flag_wrong"], blit_pos)
                elif pos in self.questionmarks:
                    self.surface.blit(self.tiles["questionmark"], blit_pos)
                else:
                    self.surface.blit(self.tiles["covered"], blit_pos)
            elif pos in self.mines:
                if pos in self.exploded_mines:
                    self.surface.blit(self.tiles["mine_exploded"], blit_pos)
                else:
                    self.surface.blit(self.tiles["mine"], blit_pos)
            else:
                self.surface.blit(self.tiles[self.hints[pos]], blit_pos)

    def update(self, mouse_pos, left_click, right_click, double_click):
        if self.game_done:
            return

        pos = ((mouse_pos[0] - self.pos[0]) // self.tile_size,
               (mouse_pos[1] - self.pos[1]) // self.tile_size)

        self.mouseover_tile = pos

        if right_click and pos in self.covered:
            self.set_mark(pos)
        elif all((left_click,
                  pos in self.covered,
                  pos not in self.flags,
                  pos not in self.questionmarks)):
            self.uncover(pos)
            self.check_defeat()
            self.check_win()
            self.refresh_surface()
        elif all((double_click,
                  pos not in self.covered,
                  self.hints.get(pos) != 0)):
            num_flags = sum((1 for n in self.neighbors[pos] if n in self.flags))
            if num_flags == self.hints[pos]:
                for neighbor in self.neighbors[pos]:
                    if all((neighbor in self.covered,
                            neighbor not in self.flags,
                            neighbor not in self.questionmarks)):
                        self.uncover(neighbor)
                self.check_defeat()
                self.check_win()
                self.refresh_surface()

    def set_mark(self, pos):
        if pos in self.flags:
            self.flags.remove(pos)
            self.questionmarks.add(pos)
        elif pos in self.questionmarks:
            self.questionmarks.remove(pos)
        else:
            self.flags.add(pos)
        self.refresh_surface()
        self.mines_remaining = self.num_mines - len(self.flags)
        self.mines_remaining_changed = True

    def uncover(self, pos):
        """Uncovers the tile at pos and all its neighbors which are not
        mines, flags or questionmarks. Uses an iterative flood fill because
        a recursive approach can exceed the maximum recursion depth.
        """
        tiles_to_uncover = {pos}
        while tiles_to_uncover:
            pos = tiles_to_uncover.pop()
            self.covered.remove(pos)
            if (pos not in self.mines) and self.hints[pos] == 0:
                for neighbor in self.neighbors[pos]:
                    if all((neighbor in self.covered,
                            neighbor not in self.flags,
                            neighbor not in self.questionmarks)):
                        tiles_to_uncover.add(neighbor)

    def check_win(self):
        if len(self.covered) == self.num_mines and not self.game_done:
            self.game_done = True
            self.end_message = "YOU WIN"

    def check_defeat(self):
        for pos in self.mines:
            if pos not in self.covered:
                self.exploded_mines.add(pos)

        if self.exploded_mines:
            self.game_done = True
            self.end_message = "GAME OVER"
            for pos in self.covered.copy():
                if all((pos in self.mines,
                        pos not in self.flags,
                        pos not in self.questionmarks)):
                    self.covered.remove(pos)
                elif (pos not in self.mines) and (pos in self.flags):
                    self.wrong_flags.add(pos)

    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        if self.mouseover_tile is not None:
            blit_pos = (self.mouseover_tile[0] * self.tile_size + self.pos[0],
                        self.mouseover_tile[1] * self.tile_size + self.pos[1])
            if self.mouseover_tile in self.flags:
                surface.blit(self.tiles["flag_highlighted"], blit_pos)
            elif self.mouseover_tile in self.questionmarks:
                surface.blit(self.tiles["questionmark_highlighted"], blit_pos)
            elif self.mouseover_tile in self.covered:
                surface.blit(self.tiles["covered_highlighted"], blit_pos)
            self.mouseover_tile = None
