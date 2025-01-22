# data_preprocessing.py
import json
import os
from constants import X_SYMBOL, O_SYMBOL, HUMAN, MACHINE

def encode_board(board):
    """Encodes a board state into a list of integers."""
    encoding = []
    for cell in board:
        if cell == " ":
            encoding.append(0)
        elif cell == X_SYMBOL:
            encoding.append(1)
        elif cell == O_SYMBOL:
            encoding.append(2)
    return encoding

def encode_player(player):
   """Encodes a player into 0 or 1"""
   if player == X_SYMBOL or player == HUMAN:
      return 1
   return 0

def encode_outcome(outcome):
    """Encodes the game outcome into a one-hot vector."""
    if outcome == X_SYMBOL:
        return [1, 0, 0]
    elif outcome == O_SYMBOL:
        return [0, 1, 0]
    elif outcome == "draw":
        return [0, 0, 1]
    return [0,0,0] # Default case

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
                games = json.load(f)

            for game in games:
                if not game:
                    continue  # Skip empty games
                last_move = game[-1]
                result = encode_outcome(last_move.get("result"))
                game_data = []
                for move_data in game:
                    if move_data.get("move") is not None:
                        encoded_board = encode_board(move_data.get("board"))
                        encoded_player = encode_player(move_data.get("player"))
                        move = move_data.get("move")
                        game_data.append((encoded_board, encoded_player, move, result))
                preprocessed_data.append(game_data)

    return preprocessed_data


def save_preprocessed_data(preprocessed_data, filename="./data/data_processed.json"):
  """Saves the preprocessed data to a JSON file."""
  with open(filename, "w") as f:
      json.dump(preprocessed_data, f, indent=4)
  print(f"Preprocessed data saved to {filename}")


if __name__ == '__main__':
    data_directory = "./data/"  # Current directory for now
    preprocessed_data = preprocess_data(data_directory)
    save_preprocessed_data(preprocessed_data)


    # Print the first elements of the data
    for element in preprocessed_data[:5]:
        print(element)

    print(f"\nTotal preprocessed moves: {len(preprocessed_data)}")