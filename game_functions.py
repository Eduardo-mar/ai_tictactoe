import random
from constants import HUMAN, MACHINE, X_SYMBOL, O_SYMBOL
from machine import get_random_move


def display_board(board, size):
    """Prints the Tic-Tac-Toe board."""
    print("---" * (size + 1))
    for i in range(size):
        row_str = "|"
        for j in range(size):
            row_str += f" {board[i * size + j]} |"
        print(row_str)
        print("---" * (size + 1))


def is_valid_move(board, move, size):
    """Checks if a move is valid."""
    if not (1 <= move <= size * size):
        print(f"Invalid move. Please enter a number between 1 and {size * size}.")
        return False
    if board[move - 1] != " ":
        print("That spot is already taken. Try again.")
        return False
    return True

def player_move(board, player_symbol, size):
    """Gets and validates the human player's move, then updates the board."""
    while True:
        try:
            move = int(input(f"Player, enter your move (1-{size*size}): "))
            if is_valid_move(board, move, size):
                board[move - 1] = player_symbol
                break
        except ValueError:
            print("Invalid input. Please enter a number.")


def check_win(board, player_symbol, size, win_size):
    """Checks if the given player has won."""
    # Check rows
    for i in range(size):
        for j in range(size - win_size + 1):
            if all(board[i * size + j + k] == player_symbol for k in range(win_size)):
                return True

    # Check columns
    for j in range(size):
        for i in range(size - win_size + 1):
            if all(board[(i + k) * size + j] == player_symbol for k in range(win_size)):
                return True
    # Check diagonals (top-left to bottom-right)
    for i in range(size - win_size + 1):
        for j in range(size - win_size + 1):
          if all(board[(i+k)*size + j + k] == player_symbol for k in range(win_size)):
            return True

    # Check diagonals (top-right to bottom-left)
    for i in range(size - win_size + 1):
        for j in range(win_size-1, size):
            if all(board[(i+k)*size + (j-k)] == player_symbol for k in range(win_size)):
                return True
    return False


def check_draw(board):
    """Checks if the game is a draw (board is full with no win)."""
    return " " not in board

def setup_game(board_size):
    """Initializes the game, choosing the first player and assigning symbols."""
    board = [" "] * (board_size * board_size)
    players = [HUMAN, MACHINE]
    first_player = random.choice(players)

    if first_player == HUMAN:
      human_player_symbol = X_SYMBOL
      machine_player_symbol = O_SYMBOL
      print(f"The human player goes first")
    else:
      human_player_symbol = O_SYMBOL
      machine_player_symbol = X_SYMBOL
      print(f"The machine player goes first")
    
    return board, first_player, human_player_symbol, machine_player_symbol

def game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition):
    """Main game loop."""
    current_player = first_player #The first player will have X symbol
    print("Let's start the game!")
    while True:
        display_board(board, board_size)
        if current_player == HUMAN:
            player_move(board, human_player_symbol, board_size)
        else:
            print("Machine is thinking...")
            move = get_random_move(board)
            if move is not None:
                board[move] = machine_player_symbol
            else:
                print("No available moves")
                break


        if check_win(board, human_player_symbol if current_player == HUMAN else machine_player_symbol, board_size, win_condition):
            display_board(board, board_size)
            if current_player == HUMAN:
                print(f"The human player wins!")
            else:
                print(f"The machine player wins!")
            break
        elif check_draw(board):
            display_board(board, board_size)
            print("It's a draw!")
            break
        else:
            # Switch players
            current_player = MACHINE if current_player == HUMAN else HUMAN