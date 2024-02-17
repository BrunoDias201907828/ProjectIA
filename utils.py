from node import Node

def possible_moves(cur_node):
    moves = []
    if cur_node.current_player == 'Black':
        for piece in cur_node.black:
            moves.append(possible(piece, cur_node.black.union(cur_node.white)))
    else:
        for piece in cur_node.white:
            moves.append(possible(piece, cur_node.black.union(cur_node.white)))
    return moves


def possible(piece, pieces):
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

print(possible_moves(Node(0, 'Black', 1, {1,3,17}, {7,21,23})))