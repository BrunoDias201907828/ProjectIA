from node import Node
import numba
import itertools
from copy import deepcopy


def possible_moves(cur_node):
    moves = []
    if cur_node.current_player == 'Black':
        for piece in cur_node.black:
            moves.append((piece, possible(piece, cur_node.black.union(cur_node.white))))
    else:
        for piece in cur_node.white:
            moves.append((piece, possible(piece, cur_node.black.union(cur_node.white))))
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

def sucessors(cur_node, new_piece, piece):
    if cur_node.current_player == 'Black':
        new_black = deepcopy(cur_node.black)
        new_black.remove(piece)
        new_black.add(new_piece)
        return Node(cur_node.depth - 1, cur_node.begin_depth, 'White', 1, deepcopy(cur_node.white), new_black)
    else:
        new_white = deepcopy(cur_node.white)
        new_white.remove(piece)
        new_white.add(new_piece)

        return Node(cur_node.depth - 1, cur_node.begin_depth, 'Black', 1, new_white, deepcopy(cur_node.black))
    

def is_winner(positions) -> bool:
    positions = sorted(positions)
    differences = {positions[1] - positions[0], positions[2] - positions[1]}
    if len(differences) != 1:
        return False
    value = differences.pop()
    if value in [1, 5, 4, 6]:  # RIGHT, DOWN, LEFT DOWN, RIGHT DOWN
        return True
    return False


@numba.njit
def _distance_score(pairs):
    score = 0
    for (p0, p1) in pairs:
        x0, y0 = p0 % 5, p0 // 5
        x1, y1 = p1 % 5, p1 // 5
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        if dx == 0 or dy == 0 or dx == dy:
            if dx == 1 or dy == 1:
                score += 3
            else:
                score += 1
    return score


def distance_score(positions):
    positions = tuple(positions)
    return _distance_score(tuple(itertools.combinations(positions, 2)))


def next_move_score(positions, enemy_position):
    score = 0
    for p in positions:
        future_positions = possible(p, positions | enemy_position)
        for fp in future_positions:
            new_positions = positions.copy()
            new_positions.remove(p)
            new_positions.add(fp)
            score += int(is_winner(new_positions))
    return score