import pygame as pg

import box
import button
import gamestate
import prepare


class Custom(gamestate.GameState):
    def __init__(self):
        super().__init__()
        self.buttons = (button.Button((self.window_size[0] // 2, 180), "PLAY",
                                      size=prepare.BIG_BUTTON_SIZE),
                        button.Button((self.window_size[0] // 2, 245), "BACK"))
        self.play_button = self.buttons[0]
        self.top_textbox_text = "Customize your Minefield"
        self.top_textbox = box.Box((280, 35), (self.window_size[0] // 2, 20),
                                   self.top_textbox_text, centerx=True)
        self.inputtexts = {"width": "width", "height": "height",
                           "mines": "mines"}
        self.inputboxes = {"width": box.Box((80, 35),
                                            (self.window_size[0] * 1 / 5, 110),
                                            self.inputtexts["width"],
                                            tiles=prepare.textbox_tiles,
                                            centerx=True,
                                            name="width"),
                           "height": box.Box((80, 35),
                                             (self.window_size[0] / 2, 110),
                                             self.inputtexts["height"],
                                             tiles=prepare.textbox_tiles,
                                             centerx=True,
                                             name="height"),
                           "mines": box.Box((80, 35),
                                            (self.window_size[0] * 4 / 5, 110),
                                            self.inputtexts["mines"],
                                            tiles=prepare.textbox_tiles,
                                            centerx=True,
                                            name="mines")}
        self.valid_chars = "0123456789"
        self.active_inputbox = None
        self.textcursor = "|"
        self.max_sidelength = 40

    def update(self, dt):
        self.update_buttons()

        if self.left_click:
            self.active_inputbox = None
            for ib in self.inputboxes.values():
                if ib.rect.collidepoint(self.mouse_pos):
                    self.active_inputbox = ib.name
                    if self.inputtexts[ib.name][-1] != self.textcursor:
                        self.inputtexts[ib.name] += self.textcursor
                else:
                    self.inputtexts[ib.name] = self.inputtexts[ib.name].replace(
                        self.textcursor, "")

        if self.keydown_events and (self.active_inputbox is not None):
            text = self.inputtexts[self.active_inputbox].replace(
                self.textcursor, "")
            for event in self.keydown_events:
                if event.unicode in self.valid_chars:
                    text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
            self.inputtexts[self.active_inputbox] = text + self.textcursor

        for key, text in self.inputtexts.items():
            if text != key:
                if not text:  # text == ""
                    text = key
                else:
                    text = text.replace(key, "")
            self.inputtexts[key] = text

        for ib in self.inputboxes.values():
            ib.update(self.inputtexts[ib.name])

        self.check_input()

    def check_input(self):
        try:
            width = int(self.inputtexts["width"].replace(self.textcursor, ""))
            height = int(self.inputtexts["height"].replace(self.textcursor, ""))
            mines = int(self.inputtexts["mines"].replace(self.textcursor, ""))
        except ValueError:
            self.play_button.locked = True
        else:
            if all((width in range(1, self.max_sidelength + 1),
                    height in range(1, self.max_sidelength + 1),
                    0 < mines <= width * height)):
                self.play_button.locked = False
                self.persist["width"] = width
                self.persist["height"] = height
                self.persist["number_of_mines"] = mines
            else:
                self.play_button.locked = True

    def button_action(self, clicked_button):
        if clicked_button.text == "BACK":
            self.next_state_name = "NewGameMenu"
        else:
            self.next_state_name = "GamePlay"
            x = self.persist["width"]*prepare.MINEFIELD_TILE_SIZE+2*3+60+220
            y = max(self.persist["height"]*prepare.MINEFIELD_TILE_SIZE+2*3+2*20,
                    2*20+3*prepare.BUTTON_SIZE[1]+35+2*15+20)
            self.persist["window_size"] = (x, y)

    def draw(self, surface):
        self.draw_buttons(surface)
        self.top_textbox.draw(surface)
        for ibox in self.inputboxes.values():
            ibox.draw(surface)
