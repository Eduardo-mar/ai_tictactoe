import random

def get_random_move(board, epsilon=0.1):
    """Gets a move using epsilon-greedy strategy."""
    available_spots = [i for i, spot in enumerate(board) if spot == " "]
    if not available_spots:
        return None

    if random.random() < epsilon:
        # Explore: Choose a random move
        return random.choice(available_spots)
    else:
        # Exploit:  Choose the best move (currently random, replace with better logic later)
        return random.choice(available_spots) # Placeholder for now.  Replace with logic to choose best known move later