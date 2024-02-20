from node import Node
from utils import *
import math

visited = set()

""" def terminal(node):
    if node.current_player == 'Black':
        if is_winner(node.black):
            return 1
    else:
        if is_winner(node.white):
            return 1
    return 0
 """
#create utility function


def eval_experimental(node, player):
    positions = getattr(node, player.lower())
    return distance_score(positions)


def eval(node, player):
    if is_winner(getattr(node, player.lower())):
        return 1 + node.depth / 10  # penalize depth (depth is decreasing remember)
    elif is_winner(getattr(node, 'black' if player.capitalize() == 'White' else 'white')):
        return -1
    return 0


def is_terminal(node):
    return any([is_winner(node.black), is_winner(node.white)]) or node.repetition >= 3 or node.depth == 0


def perform_action(node, position, new_position):
    player = node.current_player.lower()
    new_positions = getattr(node, player).copy()
    new_positions.remove(position)
    new_positions.add(new_position)
    repetition = get_repetitions(node)
    if player == 'black':
        return Node(white=node.white.copy(), black=new_positions, depth=node.depth - 1, current_player='White',
                    repetition=repetition, parent=node)
    else:
        return Node(white=new_positions, black=node.black.copy(), depth=node.depth - 1, current_player='Black',
                    repetition=repetition, parent=node)


def get_repetitions(node):
    key = (frozenset(node.white), frozenset(node.black))
    repetition = 1
    parent_node = node
    while True:
        if (frozenset(parent_node.white), frozenset(parent_node.black)) == key:
            repetition += 1
        parent_node = parent_node.parent
        if parent_node is None:
            break
    return repetition


def max_value(node: Node, player: str):
    if is_terminal(node):
        return eval(node, player), None
    value, move = -math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = min_value(perform_action(node, position, new_position), player)
            if value2 > value:
                value, move = value2, (position, new_position)
    return value, move


def min_value(node: Node, player: str):
    if is_terminal(node):
        return eval(node, player), None
    value, move = +math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = max_value(perform_action(node, position, new_position), player)
            if value2 < value:
                value, move = value2, (position, new_position)
    return value, move


def minimax(white: set, black: set, player: str, depth: int = 4):
    node = Node(white=white, black=black, depth=depth, current_player=player)
    return max_value(node, player)
    

if __name__ == '__main__':
    # value, node = max_player(Node(6, 6, 'Black', 1, {1,3,17}, {7,21,23}))
    value, move = minimax({1, 3, 17}, {7, 21, 23}, 'Black', depth=4)
    print(value, move)