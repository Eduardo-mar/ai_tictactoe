# index.py
from game_functions import setup_game, display_board, player_move, check_win, check_draw
from machine import get_best_move_mcts
from constants import HUMAN, MACHINE

def game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition):
    """Main game loop."""
    current_player = first_player #The first player will have X symbol
    print("Let's start the game!")
    while True:
        display_board(board, board_size)
        if current_player == HUMAN:
            player_move(board, human_player_symbol, board_size)
        else:
            print("Machine is thinking...")
            move = get_best_move_mcts(board)
            if move is not None:
                board[move] = machine_player_symbol
            else:
                print("No available moves")
                break


        if check_win(board, human_player_symbol if current_player == HUMAN else machine_player_symbol, board_size, win_condition):
            display_board(board, board_size)
            if current_player == HUMAN:
                print(f"The human player wins!")
            else:
                print(f"The machine player wins!")
            break
        elif check_draw(board):
            display_board(board, board_size)
            print("It's a draw!")
            break
        else:
            # Switch players
            current_player = MACHINE if current_player == HUMAN else HUMAN

def main(board_size=3, win_condition=3):
    """Main function to start the game."""
    board, first_player, human_player_symbol, machine_player_symbol = setup_game(board_size)
    game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition)

if __name__ == "__main__":
    main()