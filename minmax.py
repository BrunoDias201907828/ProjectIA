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

    #case draw
    if cur_node.repetition >= 3:
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
    

#value, node = max_player(Node(6, 6, 'Black', 1, {1,3,17}, {7,21,23}))
value, node = minimax(6, 'Black', {1,3,17}, {7,21,23})
print("Value: ", value)
print("Node: ", node.white, node.black)