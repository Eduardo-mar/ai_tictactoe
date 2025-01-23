# monte_carlo.py
import numpy as np
from constants import X_SYMBOL, O_SYMBOL
from game_functions import check_win, check_draw
from machine import get_random_move

def monte_carlo_simulation(board, player, board_size=3, original=True, original_player = " ", move_values = []):
  """
  Performs Monte Carlo simulations to estimate the value of each possible move.

  Args:
    board (list): The current board state.
    player (str): The current player (X or O).
    board_size (int, optional): The size of the board. Defaults to 3.
    num_simulations (int, optional): The number of simulations to run. Defaults to 100.

  Returns:
    list: one-hot vector with the calculated value for every possible move.
  """
  if original:
    original_player = player
    move_values = [0] * (board_size * board_size)
  
  # Iterate over each possible move
  for move_index in range(board_size * board_size):
    if board[move_index] == " ":
      breakpoint()
      #Make a copy of the board and play the current move
      temp_board = list(board)
      # breakpoint()
      temp_board[move_index] = player
      # breakpoint()

      # Check if this move is winner
      if check_win(temp_board, player, board_size, board_size):
        if player == original_player:
          move_values[move_index] += 1
        else:
          move_values[move_index] -= 1
      # Check if this move is a draw
      elif check_draw(temp_board):
        pass
      else:
        monte_carlo_simulation(temp_board, O_SYMBOL if player == X_SYMBOL else X_SYMBOL, board_size, False, original_player, move_values)

  if original:
    return calculate_probabilities(move_values)

def calculate_probabilities(move_values):
  """
  Calculates the probabilities of winning for each move with softmax.

  Args:
    move_values (list): The accumulated values for each move.

  Returns:
    list: The probabilities of winning for each move.
  """
  breakpoint()
  z = np.array(move_values)
  beta = 1
  move_probabilities = np.exp(beta * z) / np.sum(np.exp(beta * z))
  return move_probabilities
  # z_exp = [math.exp(i) for i in move_values]
  # sum_z_exp = sum(z_exp)
  # move_probabilities = [round(i / sum_z_exp, 3) for i in z_exp]
  # breakpoint()

def play_random_game(board, current_player, board_size):
  """
  Plays a random game from a given board state, until the end of the game.
  Returns the winner or None if draw.
  """
  while True:
    move = get_random_move(board)
    # breakpoint()
    if move is not None:
      board[move] = current_player
    else:
      return None  # Draw

    # breakpoint()
    if check_win(board, current_player, board_size, board_size):
      return current_player
    if check_draw(board):
      return None
    # breakpoint()
    current_player = O_SYMBOL if current_player == X_SYMBOL else X_SYMBOL


if __name__ == '__main__':
  # Example usage
  # initial_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
  # current_player = X_SYMBOL
  # probabilities = monte_carlo_simulation(initial_board, current_player)
  # print("Probabilities of win for each move",probabilities)

  initial_board = ["X", "O", "O",
                    "X", "O", "X",
                    " ", "X", " "]
  current_player = O_SYMBOL
  probabilities = monte_carlo_simulation(initial_board, current_player)
  print("Probabilities of win for each move",probabilities)