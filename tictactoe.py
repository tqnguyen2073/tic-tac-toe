"""
Tic Tac Toe Player
"""

import math
import copy

# Constants for player markers and empty cell
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    An empty 3x3 grid represented by a list of lists.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns the player whose turn is next on the board.
    Arguments:board -- The current state of the board.
    Returns:'X' if it is X's turn, 'O' if it is O's turn.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # X plays first, so if they have played fewer or equal times to O, it is X's turn
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns a set of all possible actions (i, j) available on the board.
    Arguments:board -- The current state of the board.
    Returns:A set of tuples (i, j) where 'i' and 'j' are the row and column indices of empty cells.
    """
    possible_moves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Arguments:board -- The current state of the board.
              action -- A tuple (i, j) representing the move position.
    Returns:A new board with the move applied, without modifying the original board.
    """
    i, j = action

    # Validate the action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: cell is not empty.")

    # Make a deep copy of the board
    new_board = copy.deepcopy(board)

    # Determine the current player and apply their move
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Arguments:board -- The current state of the board.
    Returns:'X' if X has won, 'O' if O has won, None otherwise.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # No winner
    return None


def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    Arguments:board -- The current state of the board.
    Returns:True if there's a winner or if the board is full, False otherwise.
    """
    # Check if there's a winner
    if winner(board) is not None:
        return True

    # Check if there are any empty spaces left
    for row in board:
        if EMPTY in row:
            return False

    # No empty spaces and no winner means the board is full and it's a tie
    return True


def utility(board):
    """
    Returns the utility of the board state.
    Arguments:board -- The current state of the board.
    Returns:1 if X has won, -1 if O has won, 0 if it's a tie.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board using the Minimax algorithm.
    Arguments:board -- The current state of the board.
    Returns:The best move (i, j) for the current player based on minimax strategy.
    """

    # If game is over, return None
    if terminal(board):
        return None

    current_player = player(board)

    # Helper function to calculate the max value for 'X'
    def max_value(board):
        # If game is over, return the utility score
        if terminal(board):
            return utility(board)

        # Set initial value to negative infinity for maximization
        v = -math.inf
        # Calculate the min value for each possible move
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    # Helper function to calculate the min value for 'O'
    def min_value(board):
        # If game is over, return the utility score
        if terminal(board):
            return utility(board)

        # Set initial value to positive infinity for minimization
        v = math.inf
        # Calculate the max value for each possible move
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    # Determine the best move for the current player
    best_action = None
    if current_player == X:
        best_value = -math.inf
        # For 'X', find the action that maximizes the minimum possible loss
        for action in actions(board):
            action_value = min_value(result(board, action))
            if action_value > best_value:
                best_value = action_value
                best_action = action
    else:
        best_value = math.inf
        # For 'O', find the action that minimizes the maximum possible gain
        for action in actions(board):
            action_value = max_value(result(board, action))
            if action_value < best_value:
                best_value = action_value
                best_action = action

    return best_action
