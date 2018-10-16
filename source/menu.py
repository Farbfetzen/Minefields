import button
import prepare
import gamestate


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
