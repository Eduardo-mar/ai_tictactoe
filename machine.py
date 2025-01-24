# machine.py
import numpy as np
import random
from monte_carlo import monte_carlo_simulation
from game_functions import check_win
from constants import X_SYMBOL, O_SYMBOL

def get_best_move_mcts(board, player, board_size=3):
    """
    Gets the best move using Monte Carlo Tree Search.

    Args:
        board (list): The current board state.
        player (str): The AI's player symbol (X or O).
        board_size (int, optional): The size of the board. Defaults to 3.

    Returns:
        int: The index of the best move (0-8), or None if no moves are available.
    """
    available_spots = [i for i, spot in enumerate(board) if spot == " "]
    if not available_spots:
        return None

    # Get move probabilities from MCTS
    probabilities = monte_carlo_simulation(board, player, board_size)

    # Choose the move with the highest probability, if is not available, choose randomly
    best_move = np.argmax(probabilities)
    if best_move not in available_spots:
        best_move = random.choice(available_spots)

    return best_move # Returns the index (0-8) of the chosen cell

def get_epsilon_move(board, current_player, epsilon=0.4):
    """Gets a move using epsilon-greedy strategy."""
    available_spots = [i for i, spot in enumerate(board) if spot == " "]
    if not available_spots:
        return None

    if random.random() < epsilon:
        # Explore: Choose a random move
        return random.choice(available_spots)
    else:
        # Choose the move if you can win (has 2 in a row and the third is empty)
        for i in available_spots:
            temp_board = list(board)
            temp_board[i] = current_player
            if check_win(temp_board, current_player, 3, 3):
                return i
        # Choose the move if the opponent can win (has 2 in a row and the third is empty)
        for i in available_spots:
            temp_board = list(board)
            temp_board[i] = X_SYMBOL if current_player == O_SYMBOL else O_SYMBOL
            if check_win(temp_board, X_SYMBOL if current_player == O_SYMBOL else O_SYMBOL, 3, 3):
                return i
        # Choose randomly
        return random.choice(available_spots)
        