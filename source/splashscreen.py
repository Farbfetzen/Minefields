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

import box
import gamestate
import prepare


class SplashScreen(gamestate.GameState):
    def __init__(self):
        super().__init__()
        self.next_state_name = "MainMenu"

        # commented because this is only needed once to create splashscreen.png:
        # self.game_name_textbox = box.Box((220, 50),
        #                                  (self.window_size[0] // 2,
        #                                   self.window_size[1] // 2 - 25),
        #                                  text="MINEFIELDS",
        #                                  font=prepare.BIG_FONT, centerx=True,
        #                                  centery=True)
        self.continue_textbox = box.Box((230, 25), (self.window_size[0] // 2,
                                                    self.window_size[1] - 50),
                                        text="click or press a key to start",
                                        font=prepare.SMALL_FONT, centerx=True,
                                        centery=True)

    def start(self, current_state_name, persistent, surface):
        super().start(current_state_name, persistent, surface)

        # same reason as above
        # self.game_name_textbox.draw(surface)
        surface.blit(prepare.SPLASHSCREEN_IMAGE, (0, 0))
        self.continue_textbox.draw(surface)

    def process_events(self, events):
        for event in events:
            if event.type in (pg.MOUSEBUTTONDOWN, pg.KEYDOWN):
                self.done = True
