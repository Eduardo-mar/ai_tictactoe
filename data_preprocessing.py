import json
import os
import numpy as np
from constants import X_SYMBOL, O_SYMBOL, HUMAN
from monte_carlo import monte_carlo_simulation

def encode_board(board, player):
    """Encodes a board state into a list of integers."""
    encoding = np.zeros(10, dtype=np.int8)  # Assuming 3x3 board
    for i, cell in enumerate(board):
        if cell == X_SYMBOL:
            encoding[i] = 1
        elif cell == O_SYMBOL:
            encoding[i] = 2
    if player == X_SYMBOL:
      encoding[9] = 1 # Encode the player
    else:
      encoding[9] = 0
    return encoding

def encode_outcome(board, player):
    """Encodes the move probabilities for the board state."""
    probabilities = monte_carlo_simulation(board, player)
    return np.array(probabilities, dtype=np.float32)

def preprocess_data(data_dir):
    """
    Transforms the raw game data into a preprocessed format.
    Applies delayed reward by propagating the game result to every move.
    """
    preprocessed_data = []

    for filename in os.listdir(data_dir):
        if filename.startswith("random_self_play_data_") and filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    games = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {filename}: {e}")
                    continue # Skip to the next file

            for game in games:
                if not isinstance(game, list) or len(game) == 0:
                    print(f"Skipping invalid game data: {game}")
                    continue  # Skip empty or invalid games
                for move_data in game:
                    if move_data.get("move") is not None:
                        encoded_board = encode_board(move_data.get("board"), move_data.get("player"))
                        move = move_data.get("move")
                        encoded_outcome = encode_outcome(move_data.get("board"), move_data.get("player"))
                        preprocessed_data.append((encoded_board, move, encoded_outcome))

        # Convert to Numpy arrays

    X = []
    Y = []
    for encoded_board, move, encoded_outcome in preprocessed_data:
        X.append(encoded_board)
        Y.append(encoded_outcome)

    X = np.array(X)
    Y = np.array(Y)
    return X,Y


def save_preprocessed_data(X,Y, filename="./data/data_processed.npz"):
  """Saves the preprocessed data to a JSON file."""
  np.savez(filename, X=X, Y=Y)
  print(f"Preprocessed data saved to {filename}")


if __name__ == '__main__':
    data_directory = "./data/"  # Current directory for now
    output_filename = "./data/data_processed.npz"
    if os.path.exists(data_directory):
        X,Y = preprocess_data(data_directory)
        save_preprocessed_data(X,Y)

        # Print the first elements of the data
        print(X[:5])

        print(f"\nTotal preprocessed moves: {len(X)}")
    else:
        print(f"Error: Data directory '{data_directory}' not found.")