import arcade
from Player import X, O

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
        self.current_state = GAME_MENU
        self.board = [['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']]
        self.players = ['X', 'O']
        self.current_turn = self.players[0]
        self.next_turn = self.players[1]
        self.x_list = []  # location of all X objects.
        self.o_list = []  # location of all O objects.
        self.center_locations = [(100, 500), (300, 500), (500, 500),
                                 (100, 300), (300, 300), (500, 300),
                                 (100, 100), (300, 100), (500, 100)]
        self.game_result = ""
        self.set_location(100, 100)
        arcade.set_background_color(arcade.color.BLACK)

    def show_board_data(self):
        for row in self.board:
            print(f"|{row[0]}|{row[1]}|{row[2]}|")

    def switch_turn(self):
        self.current_turn, self.next_turn = self.next_turn, self.current_turn

    def draw_board_grid(self):
        # todo refactor this so it's in function of the width, height of the game.
        arcade.draw_lines([(200, 0), (200, 600)], arcade.color.WHITE, 3)
        arcade.draw_lines([(400, 0), (400, 600)], arcade.color.WHITE, 3)
        arcade.draw_lines([(0, 200), (600, 200)], arcade.color.WHITE, 3)
        arcade.draw_lines([(0, 400), (600, 400)], arcade.color.WHITE, 3)

    def get_location_clicked(self, x, y):
        # todo refactor this. Try x/boxsize, y/boxsize
        # First row
        if 0 <= x < 200 and 400 <= y <= 600:
            return 1
        elif 200 <= x < 400 and 400 <= y <= 600:
            return 2
        elif 400 <= x <= 600 and 400 <= y <= 600:
            return 3
        # Second row
        elif 0 <= x < 200 and 200 <= y < 400:
            return 4
        elif 200 <= x < 400 and 200 <= y < 400:
            return 5
        elif 400 <= x <= 600 and 200 <= y < 400:
            return 6
        # Third row
        elif 0 <= x < 200 and 0 <= y < 200:
            return 7
        elif 200 <= x < 400 and 0 <= y < 200:
            return 8
        elif 400 <= x <= 600 and 0 <= y < 200:
            return 9
        else:
            return -1

    def check_if_winner(self):
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
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    return False
        return True

    def is_game_done(self):
        # Game is over if there's a winner or the board is full (= a tie).
        if self.check_if_winner():
            print(f"{self.next_turn} won!")
            self.game_result = f"{self.next_turn} won!"
            return True
        elif self.is_board_full():
            print("It's a tie.")
            self.game_result = "It's a tie."
            return True
        else:
            return False

    def draw_start_menu(self):
        arcade.draw_text("Tic Tac Toe",
                         200, 400, arcade.color.WHITE, 36, width=200, align="center")
        arcade.draw_text("Press ENTER to play.",
                         200, 250, arcade.color.WHITE, 14, width=200, align="center")

    def draw_game(self):
        self.draw_board_grid()
        # Draw the X's.
        for x in self.x_list:
            x.draw()
        # Draw the O's.
        for o in self.o_list:
            o.draw()

    def draw_game_over(self):
        arcade.draw_text("Tic Tac Toe",
                         200, 400, arcade.color.WHITE, 36, width=200, align="center")
        arcade.draw_text(self.game_result,
                         200, 300, arcade.color.WHITE, 30, width=200, align="center")
        arcade.draw_text("Press R to restart the game.",
                         200, 250, arcade.color.WHITE, 14, width=200, align="center")

    def on_draw(self):
        arcade.start_render()

        if self.current_state == GAME_MENU:
            self.draw_start_menu()
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game_over()

    def on_update(self, delta_time: float):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        # Change game state when ENTER is pressed.
        if self.current_state == GAME_MENU and symbol == arcade.key.ENTER:
            self.current_state = GAME_RUNNING

        # Close game if ESC or q is pressed on the keyboard.
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.Q:
            self.close()

        if self.current_state == GAME_OVER and symbol == arcade.key.R:
            self.current_state = GAME_MENU

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.current_state == GAME_RUNNING:
            if button == arcade.MOUSE_BUTTON_LEFT:
                location = self.get_location_clicked(x, y)
                print(f"({x},{y}) You clicked in {location}")

                # Add X or O to the correct board location if it's not filled.
                location -= 1  # Conversion from user logic to array indexing logic.
                row = location // 3
                col = location % 3
                if self.board[row][col] == 'X' or self.board[row][col] == 'O':
                    print("Box already filled! Please choose another location.")
                else:
                    self.board[row][col] = self.current_turn
                    cx, cy = self.center_locations[location]
                    if self.current_turn == 'X':
                        self.x_list.append(X(cx, cy))
                    else:
                        self.o_list.append(O(cx, cy))
                    self.switch_turn()

                self.show_board_data()
                if self.is_game_done():
                    self.current_state = GAME_OVER
                    #self.close()        # Close window if game is over.

def menu():
    choice = input('''
----- Tic Tac Toe -----
| 0: Play with CLI     |
| 1: Play with GUI |
| 2: exit              |
|----------------------|\n''')
    return choice


def setup_game():
    print("Initializing game...")
    board = create_board()
    players = create_players()
    current_turn, next_turn = init_turns(players)
    return board, players, current_turn, next_turn


def create_board():
    return [['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']]


def show_board(b):
    for row in b:
        print(f"|{row[0]}|{row[1]}|{row[2]}|")


def create_players():
    return ['X', 'O']


def init_turns(players):
    current_turn = players[0]
    next_turn = players[1]
    return current_turn, next_turn


def check_if_winner(b):
     # todo: possible to code this more efficient by only check the rows/cols/diagonals of the last move.
    is_over = False
    # Check horizontal
    for h in range(3):
        if b[h][0] == b[h][1] == b[h][2] and b[h][0] != '-':
            is_over = True
    # Check vertical
    for v in range(3):
        if b[0][v] == b[1][v] == b[2][v] and b[0][v] != '-':
            is_over = True
    # Check diagonal
    if (b[0][0] == b[1][1] == b[2][2] and b[0][0] != '-') or (b[2][0] == b[1][1] == b[0][2] and b[2][0] != '-'):
        is_over = True

    return is_over


def main_loop(board, players, cur, nxt):
    game_result = "tie"
    for t in range(9):
        show_board(board)

        # Check if there's a winner but not on the first 4 turns.
        if t > 4:
            if check_if_winner(board):
                game_result = nxt
                break

        # Get input from user and set it onto the board.
        bad_input = True
        user_options = [str(option) for option in range(1, 10)]
        while bad_input:
            inp = input(f"It's {cur} turn. Choose location 1-9: ")
            if inp in user_options:
                location = int(inp) - 1
                row = location // 3
                col = location % 3
                if board[row][col] == 'X' or board[row][col] == 'O':
                    print("Box already filled! Please choose another location.")
                    continue
                else:
                    board[row][col] = cur
                bad_input = False
            else:
                print("Bad input! Please enter a number from 1 to 9.")

        cur, nxt = switch_turn(cur, nxt)

    return game_result


def switch_turn(c, n):
    return n, c


def show_game_result(result):
    if result == "tie":
        print("It's a tie.")
    else:
        print(f"{result} won!")


def tictactoe_cli():
    board, players, current_turn, next_turn = setup_game()
    game_result = main_loop(board, players, current_turn, next_turn)
    show_game_result(game_result)


def tictactoe_gui():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()  # Run game window until user clicks on exit or game is over.


def main():
    while True:
        #choice = menu()
        choice = '1'  # quicker for development

        # Execute chosen menu option.
        if choice == '0':
            tictactoe_cli()
            break
        elif choice == '1':
            tictactoe_gui()
            break
        elif choice == '2':
            print("Exiting program")
            break
        else:
            print("Given input is not a valid choice. Try again.")


if __name__ == "__main__":
    main()
