# machine.py
import random

def get_random_move(board):
    """Gets a random move from available spots."""
    available_spots = [i for i, spot in enumerate(board) if spot == " "]
    if available_spots:
        return random.choice(available_spots)
    return None