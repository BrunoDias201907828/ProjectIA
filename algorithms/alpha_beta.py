from .utils import Node, is_terminal, possible_moves, perform_action, update_played_moves
from .heuristics import eval_no_heuristic
import math
import time


def max_value(node: Node, player: str, alpha: float, beta: float, played_moves: dict, _first=False, *, heuristic):
    if is_terminal(node, played_moves, _first):
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


def min_value(node: Node, player: str, alpha: float, beta: float, played_moves: dict, *, heuristic):
    if is_terminal(node, played_moves):
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
def minimax_pruning(white: set, black: set, player: str, played_moves: dict | None = None, depth: int = 7, heuristic=eval_no_heuristic):
    node = Node(white=white, black=black, depth=depth, current_player=player)
    return max_value(node, player, -math.inf, math.inf, played_moves, _first=True, heuristic=heuristic)


if __name__ == '__main__':
    t0 = time.time()

    _value, _move, _played_moves = minimax_pruning({1, 3, 17}, {7, 21, 23}, 'Black', depth=4)

    #-------------------no heuristic-------------------

    #depth 8 - 15 seg
    #depth 9 - 1 min

    #-------------------mobility-------------------

    #depth 7 - 16 seg
    #depth 8 - 1 min 12 seg

    #-------------------alignment-------------------

    #depth 7 - 13 seg
    #depth 8 - 2 min 24 seg

    #-------------------mobility_alignment-------------------

    #depth 7 - 38 seg
    #depth 8 - 4 min 54 seg

    print(_value, _move)