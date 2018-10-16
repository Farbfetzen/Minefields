"""Run this file to start the game.

Copyright 2015 Sebastian Henz
This project is licensed under the MIT license. See file 
LICENSE for details.

This program was written in Python 3.2.5 using PyGame 1.9.2 
and should still work with later versions of both.
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
