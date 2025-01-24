# machine_self_play.py
import random
import json
from constants import X_SYMBOL, O_SYMBOL
from game_functions import check_win, check_draw
from machine import get_best_move_mcts, get_epsilon_move


def random_self_play_data_collection(board_size=3, num_games=3000, games_per_file=1000):
    """Collects game data from random self-play."""
    # Initialization
    game_data = []  # List to hold game data
    total_games_played = 0  # Counter for total games
    games_in_file = 0  # Counter for the number of games saved in the current file
    file_counter = 1  # Counter for the file

    print("Starting Random Self-Play Data Collection...")

    while total_games_played < num_games:
        board = [" "] * (board_size * board_size)
        current_player = random.choice([X_SYMBOL, O_SYMBOL])
        current_game = []  # List to hold game data for the current game
        result = None  # Initialize result outside the loop

        while True:
            # Get the move
            move = get_epsilon_move(board, current_player)
            # The 50% of the moves will be the best move
            if random.random() < 0.5:
                move = int(get_best_move_mcts(board, current_player))
            #If there is no move, means that it is a draw
            if move is None:
                result = "draw"
                break

            # Save the current board state, player, and move (for now None, will be updated later)
            current_game.append(
                {
                    "board": list(board),  # We save a copy of the board
                    "player": current_player,
                    "move": move + 1,  # We add 1 to the move to go from 0-8 to 1-9
                    "result": None,
                }
            )
            board[move] = current_player

            # Check for win or draw
            if check_win(board, current_player, board_size, board_size):
                result = current_player  # We add the result on the last element
                break
            if check_draw(board):
                result = "draw"  # We add the result on the last element
                break

            # Switch players
            current_player = O_SYMBOL if current_player == X_SYMBOL else X_SYMBOL

        # Set the result for each move in the current game
        for move_data in current_game:
            move_data["result"] = result

        game_data.append(current_game)  # We add the current game to the game data

        total_games_played += 1
        games_in_file += 1

        if games_in_file >= games_per_file:
            filename = f"./data/random_self_play_data_{file_counter}.json"
            with open(filename, "w") as f:
                json.dump(game_data, f, indent=4)
            print(f"Saved {games_in_file} games to {filename}")
            file_counter += 1
            games_in_file = 0
            game_data = []

    # Save remaining data, if any
    if game_data:
        filename = f"./data/random_self_play_data_{file_counter}.json"
        with open(filename, "w") as f:
            json.dump(game_data, f, indent=4)
        print(f"Saved {len(game_data)} games to {filename}")

    print("Random Self-Play Data Collection Complete.")


if __name__ == "__main__":
    random_self_play_data_collection()