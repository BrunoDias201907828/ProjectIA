from node import Node
import numba


def possible_moves(cur_node: Node) -> list[tuple[int, list[int]]]:
    """Return a list of possible moves for the current player."""
    current_player = cur_node.current_player.lower()
    return [(piece, possible(piece, cur_node.black | cur_node.white)) for piece in getattr(cur_node, current_player)]


@numba.njit
def _possible(piece: int, pieces: tuple):
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
    return _possible(piece, tuple(pieces))


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


def eval(node, player, played_moves, first=False):
    depth_penalty = 1 - node.depth / 10
    if is_winner(getattr(node, player.lower())):
        return 2 - depth_penalty  # Later wins are less rewarded
    elif is_winner(getattr(node, 'black' if player.capitalize() == 'White' else 'white')):
        return -2 + depth_penalty  # Later loses are less penalized
    elif is_draw(node, played_moves, first):
        #-1 + depth_penalty  # Later draws are less penalized
        return 0
    return mobility_and_alignment(node)

def mobility_and_alignment(node):
    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)
    
    mobility_score = mobility(node) - mobility(node2)
    alignment_score = alignment_potential(node) - alignment_potential(node2)
    return 0.3 * mobility_score + 0.7 * alignment_score

def mobility(node):
    mob = 0
    for _, moves in possible_moves(node):
        for _ in moves:
            mob += 1
    return mob / 24

def alignment_potential(node):
    alignment = 0
    if node.current_player == 'White':
        pieces = node.white
    else:
        pieces = node.black
    for piece in pieces:
        for move in possible(piece, pieces):
            new_set = set(pieces)
            new_set.remove(piece)
            new_set.add(move)
            if is_winner(new_set):
                alignment += 1
    return min(alignment / 2, 1)

def is_terminal(node, played_moves, first=False):
    return any([is_winner(node.black), is_winner(node.white)]) or is_draw(node, played_moves, first) or node.depth == 0


def is_draw(node, played_moves, first=False):
    key = (frozenset(node.white), frozenset(node.black))
    if not first:
        repetition = node.repetition + played_moves.get(key, 0)
    else:
        repetition = played_moves.get(key, 0)
    return repetition >= 3


def perform_action(node, position, new_position):
    player = node.current_player.lower()
    new_positions = getattr(node, player).copy()
    new_positions.remove(position)
    new_positions.add(new_position)
    repetition = get_repetitions(node)
    if player == 'black':
        return Node(white=node.white.copy(), black=new_positions, depth=node.depth - 1, current_player='White',
                    repetition=repetition, parent=node)
    else:
        return Node(white=new_positions, black=node.black.copy(), depth=node.depth - 1, current_player='Black',
                    repetition=repetition, parent=node)


def get_repetitions(node: Node):
    key = (frozenset(node.white), frozenset(node.black))
    repetition = 1
    parent_node = node.parent
    while True:
        if parent_node is None:
            break
        if (frozenset(parent_node.white), frozenset(parent_node.black)) == key:
            repetition = parent_node.repetition + 1
            break
        parent_node = parent_node.parent
    return repetition


def update_played_moves(fn):
    def inner(white: set, black: set, player: str, played_moves: dict | None = None, **kwargs):
        if played_moves is None:  # consider first move
            played_moves = {(frozenset(white), frozenset(black)): 1}
        value, move = fn(white, black, player, played_moves, **kwargs)

        white, black = white.copy(), black.copy()
        set_changed = white if player.lower() == 'white' else black
        set_changed.remove(move[0])
        set_changed.add(move[1])

        key = (frozenset(white), frozenset(black))
        new_played_moves = played_moves.copy()
        new_played_moves[key] = played_moves.get(key, 0) + 1
        return value, move, new_played_moves
    return inner


if __name__ == '__main__':
    print(is_winner([19, 15, 23]))