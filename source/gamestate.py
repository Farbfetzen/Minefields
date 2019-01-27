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


class GameState:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state_name = None
        self.persist = {}
        self.previous_state_name = None
        self.state_name = None
        self.window_size = prepare.STANDARD_WINDOW_SIZE
        self.left_click = False
        self.right_click = False
        self.mouse_pos = (-1, -1)
        self.background_color = prepare.COLORS["background_color"]
        self.buttons = {}
        self.keydown_events = []

    def start(self, current_state_name, persistent, surface):
        """This method gets called everytime the game changes state to
        this gamestate. If you overwrite this method make sure to call
        super().start(current_state_name, persistent, surface) at the top
        before anything else.

        self.persist is a dict that carries information between states.
        """
        self.state_name = current_state_name
        self.persist = persistent
        if "window_size" in self.persist:
            self.window_size = self.persist["window_size"]
            del self.persist["window_size"]
        if surface.get_size() != self.window_size:
            pg.display.set_mode(self.window_size)
        surface.fill(self.background_color)

    def process_events(self, events):
        self.left_click = False
        self.right_click = False
        self.keydown_events = []
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                if event.button == 3:
                    self.right_click = True
            elif event.type == pg.KEYDOWN:
                self.keydown_events.append(event)

        if pg.mouse.get_focused():
            self.mouse_pos = pg.mouse.get_pos()
        else:
            self.mouse_pos = (-1, -1)

    def update(self, dt):
        self.update_buttons()

    def update_buttons(self):
        for b in self.buttons:
            b.update(self.mouse_pos, self.left_click)
            if b.clicked:
                b.clicked = False
                self.done = True
                self.button_action(b)

    def button_action(self, clicked_button):
        pass

    def draw_buttons(self, surface):
        for b in self.buttons:
            b.draw(surface)

    def draw(self, surface):
        self.draw_buttons(surface)
