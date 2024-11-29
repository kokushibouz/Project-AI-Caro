import copy
from typing import Tuple
from board import Board

#thuật toán alpha beta:
def ab_pruning( board: Board, depth: int, alpha: int, beta: int, max_player: bool) \
            -> Tuple[Board, int]:
    next_board: Board = None
    
    # nếu mức đang xét là lá
    if depth == 0 or board.victory(): 
        return board, board.evaluate()
    
    # nếu mức đang xét là max player
    elif max_player:  
        value = -2**32
        for child in board.adjacents():
            _, node_value = ab_pruning(child, depth - 1, alpha, beta, False)
            if node_value > value:
                value = node_value
                next_board = copy.deepcopy(child)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return next_board, value
    
    # nếu mức đang xét là min player
    else:  
        value = 2**32
        for child in board.adjacents():
            _, node_value = ab_pruning(child, depth - 1, alpha, beta, True)
            if node_value < value:
                value = node_value
                next_board = copy.deepcopy(child)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return next_board, value
