from utils import *

def mobility_and_alignment(node):
    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)

    mobility_score = (mobility(node) - mobility(node2)) * 5
    alignment_score = (alignment_potential(node) - alignment_potential(node2)) * 10

    return mobility_score + alignment_score

def mobility(node):
    mob = 0
    for _, moves in possible_moves(node):
        for _ in moves:
            mob += 1
    return mob

def alignment_potential(node):
    alignment = 0
    if node.current_player == 'White':
        pieces = node.white
    else:
        pieces = node.black
    for piece in pieces:
        for move in possible_set(piece, pieces):
            new_set = set(pieces)
            new_set.remove(piece)
            new_set.add(move)
            if is_winner(new_set):
                alignment += 1
    return alignment

def possible_set(piece: int, pieces: set):
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    for direction in directions:
        row, col = piece % 5, piece // 5
        dir_pos = -1
        while True:
            new_row = row + direction[0]
            new_col = col + direction[1]
            new_pos = new_col * 5 + new_row
            if 0 <= new_row < 5 and 0 <= new_col < 5 and new_pos not in pieces:
                dir_pos = new_pos
                row, col = new_row, new_col

            else:
                break  # Stop when reaching edge or encountering another piece
        if dir_pos != -1:
            moves.append(dir_pos)
    return moves

print(mobility(Node(white={1, 3, 15}, black={7, 21, 23}, depth=6, current_player='Black')))
