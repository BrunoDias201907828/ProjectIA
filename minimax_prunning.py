from node import Node
from minmax import utility, update_visited_states, is_terminal, possible_moves, perform_action
import math
import time


def max_value(node: Node, player: str, alpha: float, beta: float):
    update_visited_states(node)
    if is_terminal(node):
        return utility(node, player), None
    value, move = -math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = min_value(perform_action(node, position, new_position), player, alpha, beta)
            if value2 > value:
                value, move = value2, (position, new_position)
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
    return value, move


def min_value(node: Node, player: str, alpha: float, beta: float):
    update_visited_states(node)
    if is_terminal(node):
        return utility(node, player), None
    value, move = +math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = max_value(perform_action(node, position, new_position), player, alpha, beta)
            if value2 < value:
                value, move = value2, (position, new_position)
                beta = min(beta, value)
            if value <= alpha:
                return value, move
    return value, move


def minimax_pruning(white: set, black: set, player: str, depth: int = 6):
    node = Node(white=white, black=black, depth=depth, begin_depth=None, current_player=player, repetition=1)
    return max_value(node, player, -math.inf, math.inf)


if __name__ == '__main__':
    t0 = time.time()
    value, move = minimax_pruning({1, 3, 17}, {7, 21, 23}, 'Black', depth=6)
    print(time.time() - t0)
    print(value, move)
