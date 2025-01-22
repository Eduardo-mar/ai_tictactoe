# index.py
from game_functions import setup_game, game_loop

def main(board_size=3, win_condition=3):
    """Main function to start the game."""
    board, first_player, human_player_symbol, machine_player_symbol = setup_game(board_size)
    game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition)

if __name__ == "__main__":
    main()