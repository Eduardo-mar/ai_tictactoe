# index.py
from game_functions import setup_game, display_board, player_move, check_win, check_draw
from machine import get_best_move_mcts
from constants import HUMAN, MACHINE
import numpy as np
import tensorflow as tf

def game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition, model):
    """Main game loop."""
    current_player = first_player #The first player will have X symbol
    print("Let's start the game!")
    while True:
        display_board(board, board_size)
        if current_player == HUMAN:
            player_move(board, human_player_symbol, board_size)
        else:
            print("Machine is thinking...")
            move = get_ai_move(board, model, human_player_symbol, machine_player_symbol)
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

def get_ai_move(board, model, human_player_symbol, machine_player_symbol):
    """Gets the AI's move using the trained model, ensuring it's a valid move."""
    encoded_board = np.zeros(9, dtype=np.int8)
    for i, cell in enumerate(board):
        if cell == human_player_symbol:
            encoded_board[i] = 1
        elif cell == machine_player_symbol:
            encoded_board[i] = 2
    encoded_board = encoded_board.reshape(1, 9)  # Reshape so we have the shape that the model expects
    predicted_probs = model.predict(encoded_board, verbose=0)[0] # [0] is used to remove the shape (1,9)

    # Get move indices sorted by probability in descending order
    available_moves = [i for i, spot in enumerate(board) if spot == " "]
    if not available_moves:
         return None #No available moves
    sorted_moves_indices = np.argsort(predicted_probs)[::-1] #Sort from highest prob to lowest


    for move_index in sorted_moves_indices:
        if move_index in available_moves:
           return move_index  # Return the first valid move

    return None  # Should not happen if there are available moves, but just in case

def main(board_size=3, win_condition=3):
    """Main function to start the game."""
    board, first_player, human_player_symbol, machine_player_symbol = setup_game(board_size)
    model = tf.keras.models.load_model('./models/trained_model.h5')
    game_loop(board, first_player, human_player_symbol, machine_player_symbol, board_size, win_condition, model)

if __name__ == "__main__":
    main()