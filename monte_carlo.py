# monte_carlo.py
import random
from constants import X_SYMBOL, O_SYMBOL
from game_functions import check_win, check_draw
from machine import get_random_move

def monte_carlo_simulation(board, player, board_size=3, num_simulations=100):
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
  move_values = [0] * (board_size * board_size)
  
  for _ in range(num_simulations):
    # Iterate over each possible move
    for move_index in range(board_size * board_size):
      if board[move_index] == " ":
        # breakpoint()
        #Make a copy of the board and play the current move
        temp_board = list(board)
        # breakpoint()
        temp_board[move_index] = player
        # breakpoint()

        # Check if this move is winner
        if check_win(temp_board, player, board_size, board_size):
          move_values[move_index] += 1
          # Check if this move is a draw
        elif check_draw(temp_board):
          pass
        else:
          # Play a random game starting with that move
          winner = play_random_game(temp_board, X_SYMBOL if player == O_SYMBOL else O_SYMBOL, board_size)
          # breakpoint()

          # Update move value based on the outcome.
          if winner == player:
            move_values[move_index] +=1
          elif winner == None: #Draw
            pass
          else:
            move_values[move_index] -=1
  
  # Calculate probabilities
  total_simulations = num_simulations
  for i in range(len(move_values)):
    if move_values[i] !=0 :
      move_values[i] = (move_values[i] / total_simulations) #We get the probability
    else:
      move_values[i] = 0

  #Normalize data to create probabilities with softmax
  max_value = max(move_values)
  min_value = min(move_values)

  if max_value == min_value:
    move_probabilities = [1/ (board_size * board_size) ] * (board_size * board_size)
  else:
    move_probabilities = [(value - min_value) / (max_value - min_value) for value in move_values]


  return move_probabilities

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
  initial_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
  current_player = X_SYMBOL
  probabilities = monte_carlo_simulation(initial_board, current_player)
  print("Probabilities of win for each move",probabilities)

  initial_board = ["X", "O", "O",
                    "X", "O", "X",
                    " ", "X", " "]
  current_player = O_SYMBOL
  probabilities = monte_carlo_simulation(initial_board, current_player)
  print("Probabilities of win for each move",probabilities)