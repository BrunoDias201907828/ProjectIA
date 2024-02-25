from monte_carlo_node import *
import numba
##talvez tirar get_repetitions

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


def perform_action_mcts(node, position, new_position):
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

    
def is_draw(node, played_moves, first=False):
    key = (frozenset(node.white), frozenset(node.black))
    if not first:
        repetition = node.repetition + played_moves.get(key, 0)
    else:
        repetition = played_moves.get(key, 0)
    return repetition >= 3

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

def is_terminal(node, played_moves, first=False):
    return any([is_winner(node.black), is_winner(node.white)]) or is_draw(node, played_moves, first) or node.depth == 0

