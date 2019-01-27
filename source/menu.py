import button
import prepare
import gamestate



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


class MainMenu(gamestate.GameState):
    def __init__(self):
        super().__init__()
        self.buttons = (button.Button((self.window_size[0]//2, 90), "PLAY",
                                      size=prepare.BIG_BUTTON_SIZE),
                        button.Button((self.window_size[0]//2, 220), "QUIT"))

    def button_action(self, clicked_button):
        if clicked_button.text == "QUIT":
            self.quit = True
        elif clicked_button.text == "PLAY":
            self.next_state_name = "NewGameMenu"
            self.persist["width"] = 20
            self.persist["height"] = 20
            self.persist["number_of_mines"] = 30


class NewGameMenu(gamestate.GameState):
    def __init__(self):
        super().__init__()
        self.buttons = (button.Button((self.window_size[0]//2, 20), "SMALL"),
                        button.Button((self.window_size[0]//2, 70), "MEDIUM"),
                        button.Button((self.window_size[0]//2, 120), "BIG"),
                        button.Button((self.window_size[0]//2, 170), "CUSTOM"),
                        button.Button((self.window_size[0]//2, 245), "BACK"))

    def button_action(self, clicked_button):
        if clicked_button.text == "BACK":
            self.next_state_name = "MainMenu"
        elif clicked_button.text == "CUSTOM":
            self.next_state_name = "Custom"
        else:
            self.next_state_name = "GamePlay"
            if clicked_button.text == "SMALL":
                width, height, n_mines, window_size = 9, 9, 10, (475, 235)
            elif clicked_button.text == "MEDIUM":
                width, height, n_mines, window_size = 16, 16, 40, (622, 382)
            elif clicked_button.text == "BIG":
                width, height, n_mines, window_size = 30, 16, 75, (916, 382)
            self.persist = {"width": width,
                            "height": height,
                            "number_of_mines": n_mines,
                            "window_size": window_size}
