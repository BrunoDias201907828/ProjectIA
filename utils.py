from node import Node
import numba
import itertools
from copy import deepcopy


def possible_moves(cur_node: Node) -> list[tuple[int, list[int]]]:
    """Return a list of possible moves for the current player."""
    current_player = cur_node.current_player.lower()
    return [(piece, possible(piece, cur_node.black | cur_node.white)) for piece in getattr(cur_node, current_player)]


@numba.njit
def _possible(piece: int, pieces: numba.typed.List):
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


def possible(piece: int, pieces: set):
    return _possible(piece, numba.typed.List(pieces))


def sucessors(cur_node, new_piece, piece):
    """takes a pos, new pos and a node and returns a new node with the move made"""
    if cur_node.current_player == 'Black':
        new_black = cur_node.black.copy()
        new_black.remove(piece)
        new_black.add(new_piece)
        return Node(cur_node.depth - 1, cur_node.begin_depth, 'White', 1, cur_node.white.copy(), new_black)
    else:
        new_white = cur_node.white.copy()
        new_white.remove(piece)
        new_white.add(new_piece)
        return Node(cur_node.depth - 1, cur_node.begin_depth, 'Black', 1, new_white, cur_node.black.copy())


@numba.njit
def _is_winner(positions: tuple) -> bool:
    xs = [p % 5 for p in positions]
    ys = [p // 5 for p in positions]
    dx = {xs[1] - xs[0], xs[2] - xs[1]}
    dy = {ys[1] - ys[0], ys[2] - ys[1]}
    if len(dx) == 2 or len(dy) == 2 or dy.pop() > 1 or abs(dx.pop()) > 1:
        return False
    return True


def is_winner(positions: tuple | list | set) -> bool:
    positions = sorted(positions)
    return _is_winner(tuple(positions))


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


if __name__ == '__main__':
    print(is_winner([19, 15, 23]))