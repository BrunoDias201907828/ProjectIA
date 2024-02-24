from utils import *

#ALIGNMENT POTENTIAL

#CENTRALITY

#Mobility
def mobility(node):

    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)

    mobility1, mobility2 = 0, 0

    for _, moves in possible_moves(node):
        for i in range(len(moves)):
            mobility1 += 1

    for _, moves in possible_moves(node2):
        for i in range(len(moves)):
            mobility2 += 1

    return (mobility1 - mobility2)*5


print(mobility(Node(white={0, 10, 22}, black={4, 7, 16}, depth=6, current_player='Black')))
#OPEN LINES

def open_lines(node):
    white = node.white
    black = node.black
    white_lines = 0
    black_lines = 0
    for i in range(0, 5):
        if i in white:
            white_lines += 1
        if i in black:
            black_lines += 1
    return (white_lines - black_lines)*2