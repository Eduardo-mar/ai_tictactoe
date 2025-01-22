def display_board(board, size):
    """Prints the Tic-Tac-Toe board."""
    print("---" * size)
    for i in range(size):
        row_str = "|"
        for j in range(size):
            row_str += f" {board[i * size + j]} |"
        print(row_str)
        print("---" * size)


def player_move(board, player, size):
    """Gets and validates the player's move, then updates the board."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-{size*size}): "))
            if 1 <= move <= size*size:
                if board[move - 1] == " ":
                    board[move - 1] = player
                    break
                else:
                    print("That spot is already taken. Try again.")
            else:
                print(f"Invalid move. Please enter a number between 1 and {size*size}.")
        except ValueError:
            print("Invalid input. Please enter a number.")



def check_win(board, player, size, win_size):
    """Checks if the given player has won."""
    # Check rows
    for i in range(size):
        for j in range(size - win_size + 1):
            if all(board[i * size + j + k] == player for k in range(win_size)):
                return True

    # Check columns
    for j in range(size):
        for i in range(size - win_size + 1):
            if all(board[(i + k) * size + j] == player for k in range(win_size)):
                return True
    # Check diagonals (top-left to bottom-right)
    for i in range(size - win_size + 1):
        for j in range(size - win_size + 1):
          if all(board[(i+k)*size + j + k] == player for k in range(win_size)):
            return True

    # Check diagonals (top-right to bottom-left)
    for i in range(size - win_size + 1):
        for j in range(win_size-1, size):
            if all(board[(i+k)*size + (j-k)] == player for k in range(win_size)):
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw (board is full with no win)."""
    return " " not in board

def main(board_size=3, win_condition=3):
    """Main function to run the game."""
    board = [" "] * (board_size * board_size)  # Represents an empty board
    current_player = "X"

    while True:
        display_board(board, board_size)
        player_move(board, current_player, board_size)

        if check_win(board, current_player, board_size, win_condition):
            display_board(board, board_size)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            display_board(board, board_size)
            print("It's a draw!")
            break
        else:
            # Switch players
            current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main(board_size=4, win_condition=4)