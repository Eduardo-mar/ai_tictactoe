import numpy as np
from constants import X_SYMBOL, O_SYMBOL
from game_functions import check_win, check_draw
from machine import get_random_move

def monte_carlo_simulation(board, player, board_size=3):
  """
  Performs Monte Carlo simulations to estimate the value of each possible move.

  Args:
      board (list): The current board state.
      player (str): The current player (X or O).
      board_size (int, optional): The size of the board. Defaults to 3.

  Returns:
      list: one-hot vector with the calculated value for every possible move.
  """
  original_player = player
  # Initialize move_values as a local variable
  move_values = [0] * (board_size * board_size)

  def find_best_path(board, player, board_size=3, original=True, original_move=None, loop_n=0):
    """
    Simulates all possible moves and calculates move values.
    """
    for move_index in range(board_size * board_size):
      if board[move_index] == " ":
        # Make a copy of the board and play the current move
        temp_board = list(board)
        temp_board[move_index] = player

        # Check if this move is winner
        if check_win(temp_board, player, board_size, board_size):
          if player == original_player:
            if original:
              move_values[move_index] += 1 * temp_board.count(" ")  # Reward for winning sooner
            else: 
              move_values[original_move] += 1/loop_n
          else:
            move_values[original_move] += -1 if loop_n == 1 else 1/(loop_n**2)
        # Check if this move results in a draw
        elif check_draw(temp_board):
          move_values[original_move] += 1/(loop_n*2)
        elif loop_n < 5:
          # Recursive call for the opponent's turn
          find_best_path(temp_board, O_SYMBOL if player == X_SYMBOL else X_SYMBOL, board_size, False, move_index if original else original_move, loop_n+1)

    # Only calculate probabilities in the original call
    if original:
        for i in range(len(move_values)):
          if move_values[i] == 0 and min(move_values) < 0:
            move_values[i] = min(move_values) - 1
          elif move_values[i] == 0:
            move_values[i] = min(move_values)/10
        return calculate_probabilities(move_values)

  return find_best_path(board, player, board_size, True)


def calculate_probabilities(move_values):
  """
  Calculates the probabilities of winning for each move with softmax.

  Args:
    move_values (list): The accumulated values for each move.

  Returns:
    list: The probabilities of winning for each move.
  """
  z = np.array(move_values)
  beta = 1
  move_probabilities = np.exp(beta * z) / np.sum(np.exp(beta * z))
  return move_probabilities
  # z_exp = [math.exp(i) for i in move_values]
  # sum_z_exp = sum(z_exp)
  # move_probabilities = [round(i / sum_z_exp, 3) for i in z_exp]

def play_random_game(board, current_player, board_size):
  """
  Plays a random game from a given board state, until the end of the game.
  Returns the winner or None if draw.
  """
  while True:
    move = get_random_move(board)
    if move is not None:
      board[move] = current_player
    else:
      return None  # Draw

    if check_win(board, current_player, board_size, board_size):
      return current_player
    if check_draw(board):
      return None
    current_player = O_SYMBOL if current_player == X_SYMBOL else X_SYMBOL


if __name__ == '__main__':
  # Example usage
  # initial_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
  # current_player = X_SYMBOL
  # probabilities = monte_carlo_simulation(initial_board, current_player)
  # print("Probabilities of win for each move",probabilities)

  initial_board = ["X", "O", "X",
                    "X", "O", "X",
                    " ", "X", " "]
  current_player = O_SYMBOL
  probabilities = monte_carlo_simulation(initial_board, current_player)
  print("Probabilities of win for each move",probabilities)
  print("Best move:", np.argmax(probabilities)+1)                  