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

