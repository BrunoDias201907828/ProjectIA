from node import Node
from utils import *
import math

visited = set()
begin_depth = 6



def max_player(cur_node, depth):

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

    #case draw
    if cur_node.repetition >= 3:
        return 0, cur_node

    #on depth add utility value, temp it's 0
    if cur_node.depth == 0:
        return 0, cur_node

    best_value = -math.inf

    possible = possible_moves(cur_node)
    for i in range(3):
        
        (piece, moves) = possible[i]

        for new_piece in moves:
            new_node = sucessors(cur_node, new_piece, piece)
            value, node = min_player(new_node, deepcopy(new_node.depth))
            if depth == begin_depth:
                print(node.white, node.black, value, depth)
            if value > best_value:
                best_value = value
                if depth == begin_depth:
                    best_node = node
                    print("Best node: ", best_node.white, best_node.black, best_value, depth)

    return best_value, best_node

def min_player(cur_node, depth):

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
            value, node = max_player(new_node, deepcopy(new_node.depth))
            if depth == begin_depth:
                print(node.white, node.black, value, depth)
            if value < best_value:
                best_value = value
                if depth == begin_depth:
                    best_node = node

    return best_value, best_node


value, node = max_player(Node(begin_depth, 'Black', 1, {1,3,17}, {7,21,23}), begin_depth)

print("Value: ", value)
print("Node: ", node.white, node.black)