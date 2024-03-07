import functools
from .utils import possible_moves, possible, is_winner, Node, is_draw, is_terminal


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


def mobility_diff(node):
    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)
    return mobility(node) - mobility(node2)


def alignment_diff(node):
    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)
    return alignment_potential(node) - alignment_potential(node2)


def mobility_and_alignment(node):
    next_player = 'White' if node.current_player == 'Black' else 'Black'
    node2 = Node(white=node.white, black=node.black, depth=node.depth, current_player=next_player)

    mobility_score = mobility(node) - mobility(node2)
    alignment_score = alignment_potential(node) - alignment_potential(node2)
    return 0.3 * mobility_score + 0.7 * alignment_score


def eval(node, player, played_moves, first=False, fn=mobility_and_alignment):
    depth_penalty = 1 - node.depth / 10
    if is_winner(getattr(node, player.lower())):
        return 2 - depth_penalty  # Later wins are less rewarded
    if is_winner(getattr(node, 'black' if player.capitalize() == 'White' else 'white')):
        return -2 + depth_penalty  # Later loses are less penalized
    if is_draw(node, played_moves, first):
        if fn is not None:
            return 0
        return -1 + depth_penalty
    if fn is not None:
        return fn(node)
    return 0


eval_mobility = functools.partial(eval, fn=mobility_diff)
eval_alignment = functools.partial(eval, fn=alignment_diff)
eval_mobility_alignment = functools.partial(eval, fn=mobility_and_alignment)
eval_no_heuristic = functools.partial(eval, fn=None)


def cutoff_test(node, played_moves, first=False):
    if is_terminal(node, played_moves, first):
        return True
    elif eval_mobility_alignment(node, node.current_player, played_moves, first) < -0.5 and not first:
        return True
    else:
        return False
