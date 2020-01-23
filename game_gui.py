import arcade
from Player import X, O
from math import floor

# Game settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tic Tac Toe"

# Game states
GAME_MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.box_size = self.width / 3
        self.current_state = None
        self.game_result = None
        self.board = None
        self.players = None
        self.current_turn = None
        self.next_turn = None
        self.x_list = None  # location of all X objects.
        self.o_list = None  # location of all O objects.
        self.center_locations = None  # center coordinates of all board locations.

        # Set the start location of the window and its background color.
        self.set_location(100, 100)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.current_state = GAME_MENU
        self.game_result = ""
        self.board = [['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']]
        self.players = ['X', 'O']
        self.current_turn = self.players[0]
        self.next_turn = self.players[1]
        self.x_list = []
        self.o_list = []
        self.center_locations = self.get_center_locations(self.width, self.height)
        # self.center_locations = [[(100, 500), (300, 500), (500, 500)],
        #                          [(100, 300), (300, 300), (500, 300)],
        #                          [(100, 100), (300, 100), (500, 100)]]

    def get_center_locations(self, w, h):
        """ Return a 2D list of tuples.
        This 2D list contains the center coordinate (x, y) for each box in the board grid.
        Input: width and height of the board grid."""
        box = int(w / 3)
        half = int(box / 2)
        center_locations = []

        for row in range(w-half, half - 1, -box):
            tmp = []
            for col in range(half, w - half + 1, box):
                tmp.append((col, row))
            center_locations.append(tmp)
        return center_locations

    def show_board_data(self):
        """ Print the board grid with X's and O's in the terminal. """
        for row in self.board:
            print(f"|{row[0]}|{row[1]}|{row[2]}|")
        print("")

    def switch_turn(self):
        self.current_turn, self.next_turn = self.next_turn, self.current_turn

    def draw_board_grid(self, w, h, offset=0):
        """ Draw the board grid with 4 lines.
         Input: width and height of the board grid.
                offset is added to place the grid in the center for example (this is used in the game-over screen)."""
        bs = w / 3    # box size
        bs2 = bs * 2  # double box size

        # Add the offset.
        w += offset
        h += offset
        bs += offset
        bs2 += offset
        # Draw the lines.
        arcade.draw_line(bs,     offset, bs,  h,   arcade.color.WHITE, 3)  # vertical line left
        arcade.draw_line(bs2,    offset, bs2, h,   arcade.color.WHITE, 3)  # vertical line right
        arcade.draw_line(offset, bs,     w,   bs,  arcade.color.WHITE, 3)  # horizontal line top
        arcade.draw_line(offset, bs2,    w,   bs2, arcade.color.WHITE, 3)  # horizontal line bottom
        # arcade.draw_lines([(200, 0), (200, 600)], arcade.color.WHITE, 3)
        # arcade.draw_lines([(400, 0), (400, 600)], arcade.color.WHITE, 3)
        # arcade.draw_lines([(0, 200), (600, 200)], arcade.color.WHITE, 3)
        # arcade.draw_lines([(0, 400), (600, 400)], arcade.color.WHITE, 3)

    def get_location_clicked(self, x, y):
        """ Convert clicked mouse coordinates to row and column indexes for the board grid.
        Note: Coordinate (0,0) starts in bottom left corner in the arcade library. That's why we flip
        the y-axis in the calculation. Otherwise the row index in the board is flipped. """
        col = floor(x / self.box_size)
        row = floor(abs(y-self.height) / self.box_size)
        return row, col

    def check_if_winner(self):
        """ Check if there's a winner by checking if there are 3 same characters
        on a horizontal, vertical or diagonal line and different from an empty box ('-'). """
        b = self.board
        # Check horizontal
        for h in range(3):
            if b[h][0] == b[h][1] == b[h][2] and b[h][0] != '-':
                return True
        # Check vertical
        for v in range(3):
            if b[0][v] == b[1][v] == b[2][v] and b[0][v] != '-':
                return True
        # Check diagonal
        if (b[0][0] == b[1][1] == b[2][2] and b[0][0] != '-') or (b[2][0] == b[1][1] == b[0][2] and b[2][0] != '-'):
            return True

    def is_board_full(self):
        """ Check if the board is completely filled in. """
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    return False
        return True

    def is_game_done(self):
        """ Check if the game is over. The game is over if there's a winner of the board if full (= a tie). """
        if self.check_if_winner():
            print(f"Player {self.next_turn} won!")
            self.game_result = f"Player {self.next_turn} won!"
            return True
        elif self.is_board_full():
            print("It's a tie.")
            self.game_result = "It's a tie."
            return True
        else:
            return False

    def draw_start_menu(self):
        """ Draw the start menu, so drawing a title and drawing instructions to start or exit the game. """
        arcade.draw_text("Tic Tac Toe",
                         0, 400, arcade.color.WHITE, 36, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("Press ENTER to play.",
                         0, 200, arcade.color.WHITE, 14, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("Press ESC or Q at any time to quit the game.",
                         0, 150, arcade.color.WHITE, 14, width=SCREEN_WIDTH, align="center")

    def draw_game(self):
        """ Draw the game, so draw the board grid and draw the X's and O's. """
        self.draw_board_grid(self.width, self.height)
        # Draw the X's.
        for x in self.x_list:
            x.draw()
        # Draw the O's.
        for o in self.o_list:
            o.draw()

    def draw_game_over(self):
        """ Draw the game over screen, so drawing the game result (winner or tie), draw a smaller version
        of the board grid with it's X's and O's in the center of the screen and drawing instructions to restart
        or exit the game. """
        arcade.draw_text(self.game_result,
                         0, 450, arcade.color.WHITE, 36, width=SCREEN_WIDTH, align="center")

        # Draw small board_grid in the center and draw the (small) X's & O's in the grid. To place the grid,
        # X's and O's in the center, an offset is used.
        BOARD_WIDTH_SMALL = 180
        BOARD_HEIGHT_SMALL = 180
        BOARD_OFFSET_SMALL = 210
        self.draw_board_grid(BOARD_WIDTH_SMALL, BOARD_HEIGHT_SMALL, BOARD_OFFSET_SMALL)
        locations = self.get_center_locations(BOARD_WIDTH_SMALL, BOARD_HEIGHT_SMALL)
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                cx, cy = locations[i][j]
                cx += BOARD_OFFSET_SMALL
                cy += BOARD_OFFSET_SMALL
                if col == 'X':
                    x = X(cx, cy)
                    x.size = 20
                    x.draw()
                elif col == 'O':
                    o = O(cx, cy)
                    o.radius = 20
                    o.draw()
                else:
                    continue

        arcade.draw_text("Press R to restart the game.",
                         0, 150, arcade.color.WHITE, 14, width=SCREEN_WIDTH, align="center")
        arcade.draw_text("Press ESC or Q to exit the game.",
                         0, 100, arcade.color.WHITE, 14, width=SCREEN_WIDTH, align="center")

    def on_draw(self):
        """ Render the screen. All drawing code goes here. """
        arcade.start_render()  # Required to be called before drawing anything to the screen.

        # Draw the menu, game, or game-over screen depending on the game state.
        if self.current_state == GAME_MENU:
            self.draw_start_menu()
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game_over()

    def on_update(self, delta_time: float):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """ Called when the user releases a key. """
        # Change game state when ENTER is pressed.
        if self.current_state == GAME_MENU and symbol == arcade.key.ENTER:
            self.current_state = GAME_RUNNING

        # Close game if ESC or q is pressed on the keyboard.
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.Q:
            self.close()

        # Change game state when R is pressed.
        if self.current_state == GAME_OVER and symbol == arcade.key.R:
            self.setup()
            self.current_state = GAME_MENU

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Called when left mouse button is pressed. """
        if self.current_state == GAME_RUNNING:
            if button == arcade.MOUSE_BUTTON_LEFT:
                # Translate mouse coordinates to row, col indexes for the tic tac toe board.
                row, col = self.get_location_clicked(x, y)

                # Add X or O to the correct board location if it's not filled.
                if self.board[row][col] == 'X' or self.board[row][col] == 'O':
                    print("Box already filled! Please choose another location.")
                else:
                    # Fill an X or O in the board and add an X or O object in the list depending on the current turn.
                    # The X and O lists are later used to draw them on the screen.
                    self.board[row][col] = self.current_turn
                    cx, cy = self.center_locations[row][col]
                    if self.current_turn == 'X':
                        self.x_list.append(X(cx, cy))
                    else:
                        self.o_list.append(O(cx, cy))
                    self.switch_turn()

                self.show_board_data()

                if self.is_game_done():
                    self.current_state = GAME_OVER


def tictactoe_gui():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()  # Run game window until user exits the game.