def menu():
    choice = input('''
----- Tic Tac Toe -----
| 0: Play with CLI     |
| 1: Play Toe with GUI |
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


def main():
    while True:
        choice = menu()

        # Execute chosen menu option.
        if choice == '0':
            tictactoe_cli()
        elif choice == '1':
            pass
        elif choice == '2':
            print("Exiting program")
            break
        else:
            print("Given input is not a valid choice. Try again.")


if __name__ == "__main__":
    main()
