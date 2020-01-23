import game_cli  # Import the CLI Tic Tac Toe game.
import game_gui  # Import the GUI Tic Tac Toe game.


def menu():
    choice = input('''
----- Tic Tac Toe -----
| 0: Play with CLI     |
| 1: Play with GUI |
| 2: exit              |
|----------------------|\n''')
    return choice


def main():
    while True:
        choice = menu()
        #choice = '1'  # quicker for gui development

        # Execute chosen menu option.
        if choice == '0':
            game_cli.tictactoe_cli()
            break
        elif choice == '1':
            game_gui.tictactoe_gui()
            break
        elif choice == '2':
            print("Exiting program")
            break
        else:
            print("Given input is not a valid choice. Try again.")


if __name__ == "__main__":
    main()
