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

visited_states = set()


def update_visited_states(node):
    white = frozenset(node.white)
    black = frozenset(node.black)
    if (white, black) in visited_states:
        node.repetition += 1
    else:
        visited_states.add((white, black))


def utility_experimental(node, player):
    positions = getattr(node, player.lower())
    return distance_score(positions)


def utility(node, player):
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
    if player == 'black':
        return Node(white=node.white.copy(), black=new_positions, depth=node.depth - 1, begin_depth=node.begin_depth,
                    current_player='White', repetition=1)
    else:
        return Node(white=new_positions, black=node.black.copy(), depth=node.depth - 1, begin_depth=node.begin_depth,
                    current_player='Black', repetition=1)


def max_value_experimental(node: Node, player: str):
    update_visited_states(node)
    if is_terminal(node):
        return utility(node, player), None
    value, move = -math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = min_value_experimental(perform_action(node, position, new_position), player)
            if value2 > value:
                value, move = value2, (position, new_position)
    return value, move


def min_value_experimental(node: Node, player: str):
    update_visited_states(node)
    if is_terminal(node):
        return utility(node, player), None
    value, move = +math.inf, None
    for position, moves in possible_moves(node):
        for new_position in moves:
            value2, _ = max_value_experimental(perform_action(node, position, new_position), player)
            if value2 < value:
                value, move = value2, (position, new_position)
    return value, move


def minimax_experimental(white: set, black: set, player: str, depth: int = 5):
    node = Node(white=white, black=black, depth=depth, begin_depth=None, current_player=player, repetition=1)
    return max_value_experimental(node, player)


def max_player(cur_node):

    best_node = cur_node

    white = frozenset(cur_node.white)
    black = frozenset(cur_node.black)

    if (white, black) in visited:
        cur_node.repetition += 1
    else:
        visited.add((white, black))
    
    if cur_node.current_player == 'Black':
        if is_winner(cur_node.black):
            return 1, cur_node
    else:
        if is_winner(cur_node.white):
            return 1, cur_node    

    if cur_node.repetition >= 3:  # draw
        return 0, cur_node

    #on depth add utility value, temp it's 0
    #if cur_node.depth == 0 or terminal(node):
    #    return 0, cur_node

    if cur_node.depth == 0:
        return 0, cur_node

    best_value = -math.inf

    possible = possible_moves(cur_node)
    for i in range(3):
        
        (piece, moves) = possible[i]

        for new_piece in moves:
            new_node = sucessors(cur_node, new_piece, piece)
            value, node = min_player(new_node)

            if value > best_value:
                best_value = value
                if cur_node.depth == cur_node.begin_depth:
                    best_node = node
                    print("Best node: ", best_node.white, best_node.black, best_value, cur_node.depth)

    return best_value, best_node


def min_player(cur_node):

    best_node = cur_node

    white = frozenset(cur_node.white)
    black = frozenset(cur_node.black)

    if (white, black) in visited:
        cur_node.repetition += 1
    else:
        visited.add((white, black))

    if cur_node.current_player == 'Black':
        if is_winner(cur_node.black):
            return -1, cur_node
    else:
        if is_winner(cur_node.white):
            return -1, cur_node
    
    #case draw
    if cur_node.repetition >= 3:
        return 0, cur_node
    
    #on depth add utility value, temp it's 0
    if cur_node.depth == 0:
        return 0, cur_node

    best_value = +math.inf

    possible = possible_moves(cur_node)
    for i in range(3):
        (piece, moves) = possible[i]
        
        for new_piece in moves:
            new_node = sucessors(cur_node, new_piece, piece)
            value, node = max_player(new_node)
  
            if value < best_value:
                best_value = value
                if cur_node.depth == cur_node.begin_depth:
                    best_node = node

    return best_value, best_node


def minimax(depth, current_player, white, black):    
    return max_player(Node(depth, depth, current_player, 1, white, black))
    

if __name__ == '__main__':
    # value, node = max_player(Node(6, 6, 'Black', 1, {1,3,17}, {7,21,23}))
    value, node = minimax(5, 'Black', {1,3,17}, {7,21,23})
    print("Value: ", value)
    print("Node: ", node.white, node.black)

    value, move = minimax_experimental({1, 3, 17}, {7, 21, 23}, 'Black', depth=5)
    print(value, move)
