from node import Node
from minmax import eval, possible_moves, perform_action, update_played_moves, cutoff_test, eval_alignment, eval_mobility, eval_mobility_alignment, eval_no_heuristic
import math
import time


def max_value(node: Node, player: str, alpha: float, beta: float, played_moves: dict, _first=False, heuristic=eval_no_heuristic):
    if cutoff_test(node, played_moves, _first):
        return heuristic(node, player, played_moves, first=_first), None
    value, move = -math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = min_value(perform_action(node, position, new_position), player, alpha, beta, played_moves, heuristic=heuristic)
            if value2 > value:
                value, move = value2, (position, new_position)
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
    return value, move


def min_value(node: Node, player: str, alpha: float, beta: float, played_moves: dict, heuristic=eval_no_heuristic):
    if cutoff_test(node, played_moves):
        return heuristic(node, player, played_moves), None
    value, move = +math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = max_value(perform_action(node, position, new_position), player, alpha, beta, played_moves, heuristic=heuristic)
            if value2 < value:
                value, move = value2, (position, new_position)
                beta = min(beta, value)
            if value <= alpha:
                return value, move
    return value, move  # move is a tupple with position of the piece (startpos you want to play and endpos) 0-24


@update_played_moves
<<<<<<< HEAD
def last_prunning(white: set, black: set, player: str, played_moves: dict | None = None, depth: int = 6, heuristic=eval_no_heuristic):

=======
def minimax_pruning(white: set, black: set, player: str, played_moves: dict | None = None, depth: int = 6, heuristic=eval_mobility):
>>>>>>> 3d247e931749148eea47a523480ca9b4feb800bc
    node = Node(white=white, black=black, depth=depth, current_player=player)
    return max_value(node, player, -math.inf, math.inf, played_moves, _first=True, heuristic=heuristic)


if __name__ == '__main__':
    t0 = time.time()
    _value, _move, _played_moves = last_prunning({1, 3, 17}, {7, 21, 23}, 'Black', depth=8)

        #-------------------no heuristic-------------------

    #depth 8 - 4 seg
    #depth 9 - 7 seg
    #depth 10 - 13 seg
    #depth 11 - 36 seg
    #depth 12 - 1 min 35 seg

    #-------------------mobility-------------------

    #depth 7 - 10 seg
    #depth 8 - 42 seg
    #depth 9 - 2 min 36 seg

    #-------------------alignment-------------------

    #depth 7 - 4 seg
    #depth 8 - 11 seg
    #depth 9 - 20 seg
    #depth 10 - 1 min 31 seg

    #-------------------mobility_alignment-------------------

    #depth 7 - 10 seg
    #depth 8 - 1 min

    print(_value, _move)

    #performance vou usar no_heuristic(d=12), mobility(d=8), alignment(d=10), mobility_alignment(d=8)