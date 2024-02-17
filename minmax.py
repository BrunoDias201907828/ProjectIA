from node import Node
from utils import *
import math

visited = set()

def max_player(cur_node):

    #draw method

    visited.get(cur_node, -1)

    #win/lose method

    if 

    best_value = -math.inf

    possible = possible_moves(cur_node)
    for i in range(3):
        (piece, moves) = possible[i]
        
        for new_piece in range(len(moves)):
            new_node = sucessors(cur_node, new_piece, piece)
            value = min_player(new_node)

            best_value = max(value, best_value)
    
    return  best_value

def min_player(cur_node):
    return 0

     





""" 
set.add(cur_node)



max(Node cur_node):
    for i in visited:
        if cur_node.white == i.white and cur_node.black == i.black:
            i.repetition += 1
            break

        set.add(cur_node)

 """