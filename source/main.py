"""Run this file to start the game.

Copyright (C) 2019 Sebastian Henz

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


import sys

import pygame as pg

import prepare  # needs to be imported first to ensure correct initialization
import custom
import gameplay
import menu
import splashscreen


states = {"Custom": custom.Custom(),
          "GamePlay": gameplay.GamePlay(),
          "NewGameMenu": menu.NewGameMenu(),
          "MainMenu": menu.MainMenu(),
          "SplashScreen": splashscreen.SplashScreen()}
state = states[prepare.START_STATE_NAME]
state.start(prepare.START_STATE_NAME, {}, pg.display.get_surface())
clock = pg.time.Clock()


if __name__ == "__main__":
    while True:
        dt = clock.tick(prepare.FPS_MAX)  # in milliseconds
        if pg.event.get(pg.QUIT) or state.quit:
            break
        state.process_events(pg.event.get())
        if state.done:
            state.done = False
            persistent = state.persist
            next_state_name = state.next_state_name
            state = states[next_state_name]
            state.start(next_state_name, persistent, prepare.display_surface)
        state.update(dt)
        state.draw(prepare.display_surface)
        pg.display.update()

    pg.quit()
    sys.exit()
