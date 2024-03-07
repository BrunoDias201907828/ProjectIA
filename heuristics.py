from utils import possible_moves, possible, is_winner, Node


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
