from utils import is_terminal, possible_moves, perform_action, update_played_moves, Node
from heuristics import eval, eval_mobility, eval_alignment, eval_mobility_alignment, eval_no_heuristic, cutoff_test

import math


def max_value(node: Node, player: str, played_moves: dict, _first=False):
    if is_terminal(node, played_moves, first=_first):
        return eval_no_heuristic(node, player, played_moves, first=_first), None
    value, move = -math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = min_value(perform_action(node, position, new_position), player, played_moves)
            if value2 > value:
                value, move = value2, (position, new_position)
    return value, move


def min_value(node: Node, player: str, played_moves: dict):
    if is_terminal(node, played_moves):
        return eval_no_heuristic(node, player, played_moves), None
    value, move = +math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = max_value(perform_action(node, position, new_position), player, played_moves)
            if value2 < value:
                value, move = value2, (position, new_position)
    return value, move


@update_played_moves
def minimax(white: set, black: set, player: str, played_moves: dict | None = None, depth: int = 6):
    node = Node(white=white, black=black, depth=depth, current_player=player)
    return max_value(node, player, played_moves, _first=True)


if __name__ == '__main__':
    # value, node = max_player(Node(6, 6, 'Black', 1, {1,3,17}, {7,21,23}))
    _value, _move, _played_moves = minimax({1, 3, 17}, {7, 21, 23}, 'Black', depth=5)
    #depth 5 - 15seg
    #depth 6 - 1min
    print(_value, _move)
    print(_played_moves)
