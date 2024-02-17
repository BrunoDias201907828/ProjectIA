from node import Node

def possible_moves(cur_node):
    moves = []
    if cur_node.current_player == 'Black':
        for piece in cur_node.black:
            moves.append(piece, possible(piece, cur_node.black.union(cur_node.white)))
    else:
        for piece in cur_node.white:
            moves.append(piece, possible(piece, cur_node.black.union(cur_node.white)))
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

#sucessors - takes a pos, new pos and a node and returns a new node with the move made

def sucessors(cur_node, pos, piece):
    if cur_node.current_player == 'Black':
        new_black = cur_node.black.copy()
        new_black.remove(piece)
        new_black.add(pos)
        return Node(cur_node.depth - 1, 'White', cur_node.repetition, cur_node.white, new_black)
    else:
        new_white = cur_node.white.copy()
        new_white.remove(piece)
        new_white.add(pos)
        return Node(cur_node.depth - 1, 'Black', cur_node.repetition, new_white, cur_node.black)
    


print(sucessors(Node(0, 'Black', 1, {1,3,17}, {7,21,23}), 9, 7).black)

print(possible_moves(Node(0, 'Black', 1, {1,3,17}, {7,21,23})))