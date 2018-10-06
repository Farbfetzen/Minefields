import box
import button
import minefield
import prepare
import gamestate


class GamePlay(gamestate.GameState):
    def __init__(self):
        super().__init__()
        self.minefield = None
        self.minefield_rect = None
        self.right_click = False
        self.double_left_click = False
        self.double_click_timer = 0
        self.max_double_click_time = 400  # milliseconds
        self.textbox = None
        self.win_lose_announced = False

    def start(self, current_state_name, persistent, surface):
        super().start(current_state_name, persistent, surface)

        self.minefield = minefield.Minefield(self.persist["width"],
                                             self.persist["height"],
                                             self.persist["number_of_mines"])
        self.minefield.pos = (20 + prepare.box_tiles["width"],
                              20 + prepare.box_tiles["height"])
        self.minefield_rect = self.minefield.surface.get_rect(
            topleft=self.minefield.pos)

        border = box.Box(
            (self.minefield_rect.width + 2 * prepare.box_tiles["width"],
             self.minefield_rect.height + 2 * prepare.box_tiles["height"]),
            (self.minefield_rect.topleft[0] - prepare.box_tiles["width"],
             self.minefield_rect.topleft[1] - prepare.box_tiles["height"]))
        border.draw(surface)

        mines_remaining = "{} mine{} remaining".format(
            self.minefield.mines_remaining,
            "s" if self.minefield.mines_remaining != 1 else "")
        textbox_size = (220, 35)
        self.textbox = box.Box(textbox_size,
                               (self.window_size[0] - (20+textbox_size[0]), 20),
                               text=mines_remaining)

        self.buttons = {
            button.Button((self.window_size[0] - (20 + prepare.BUTTON_SIZE[0]),
                           textbox_size[1] + 40), "NEW", centerx=False),
            button.Button((self.window_size[0] - (20 + prepare.BUTTON_SIZE[0]),
                           textbox_size[1] + 90), "MENU", centerx=False),
            button.Button((self.window_size[0] - (20 + prepare.BUTTON_SIZE[0]),
                           textbox_size[1] + 140), "QUIT", centerx=False)}

        self.win_lose_announced = False

    def update(self, dt):
        self.double_left_click = False
        if (self.left_click and
                0 < self.double_click_timer <= self.max_double_click_time):
            self.double_left_click = True
        if self.double_click_timer > self.max_double_click_time:
            self.double_click_timer = 0
        if self.left_click or self.double_click_timer > 0:
            self.double_click_timer += dt

        # Highlight tile when mouse is over it:
        if self.minefield_rect.collidepoint(self.mouse_pos):
            self.minefield.update(self.mouse_pos, self.left_click,
                                  self.right_click, self.double_left_click)

        if self.minefield.mines_remaining_changed:
            self.minefield.mines_remaining_changed = False
            mines_remaining = "{} mine{} remaining".format(
                self.minefield.mines_remaining,
                "s" if self.minefield.mines_remaining != 1 else "")
            self.textbox.update(mines_remaining)

        if self.minefield.game_done and not self.win_lose_announced:
            self.textbox.update(self.minefield.end_message)
            self.win_lose_announced = True

        self.update_buttons()

    def button_action(self, clicked_button):
        if clicked_button.text == "NEW":
            self.next_state_name = "GamePlay"
        elif clicked_button.text == "MENU":
            self.next_state_name = "NewGameMenu"
        elif clicked_button.text == "QUIT":
            self.quit = True

    def draw(self, surface):
        self.draw_buttons(surface)
        self.minefield.draw(surface)
        self.textbox.draw(surface)
