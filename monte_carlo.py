import random
import time
from utils import update_played_moves
from utils_mcts import *


def resources_left(start_time, time_limit):
    return time.time() - start_time < time_limit


def monte_carlo_tree_search(root_node, played_moves, time_limit=30, player='Black'):
    """ Perform MCTS constrained by time limit. """
    start_time = time.time()

    root_node.create_children()
    for child in (child for child in root_node.children if child.is_winner(player)):
        return child
    root_node.remove_terminal_children(played_moves)

    while resources_left(start_time, time_limit):  # ou entao por numero de simulaçoes
        leaf, simulation_result = selection(root_node, player, played_moves)
        if simulation_result < 0:
            child, simulation_result = expand(leaf, 2, player, played_moves)
            if simulation_result < 0:
                simulation_result = rollout(child, played_moves, player)
            backpropagate(child, simulation_result, player)
        else:
            backpropagate(leaf, simulation_result, player)
    return best_child(root_node)


def selection(node, player, played_moves):
    """ Perform Selection until selection depth is reached, using the UCT selection policy. """
    while fully_expanded(node):
        node = best_uct(node)
        if node.is_terminal(played_moves):
            return node, result(node, player)
    return node, -1


def fully_expanded(node):
    if len(node.children) == 0:
        return False  # No children to expand
    return True


def best_uct(node):
    """ Choose the best children to explore based on the UCT value. """
    uct_values = [child.uct for child in node.children]
    indexes = [i for i, uct in enumerate(uct_values) if uct == max(uct_values)]
    child = node.children[random.choice(indexes)]
    return child


def expand(node, n_child, player, played_moves):
    """ Expand the node by adding a new child. """
    possible = possible_moves(node)
    children = []
    for _ in range(n_child):
        possible = [(p, m) for p, m in possible if m]
        position, new_positions = random.choice(possible)
        new_position = random.choice(new_positions)
        new_positions.remove(new_position)
        child = perform_action_mcts(node, position, new_position)
        children.append(child)
        if child.is_terminal(played_moves):
            node.children.extend(children)
            return child, result(child, player)
    node.children.extend(children)
    return random.choice(children), -1


def rollout(node, played_moves, player):
    """ Rollout with Random Choice as the Playout Policy. """
    while not is_terminal(node, played_moves):
        position, new_positions = random.choice([(p, m) for p, m in possible_moves(node) if m])
        new_position = random.choice(new_positions)
        node = perform_action_mcts(node, position, new_position)
    return result(node, player)


def result(node, player):
    if is_winner(getattr(node, player.lower())):
        return 1
    if is_winner(getattr(node, 'white' if player.lower() == 'black' else 'black')):
        return 0
    return 0.5


def backpropagate(node, result, player):
    if node is None:
        return
    node.visits += 1
    if node.current_player != player:
        node.utility += result
    else:
        node.utility += 1 - result
    backpropagate(node.parent, result, player)


def best_child(node):
    """ Choose the best child of a node based on the number of visits. """
    best_child = max(node.children, key=lambda child: child.visits)
    return best_child


@update_played_moves
def mcts(white: set, black: set, player: str, played_moves: dict | None = None, time_limit: int = 30):
    init_node = Node(current_player=player, white=white, black=black)
    node = monte_carlo_tree_search(init_node, played_moves, time_limit=time_limit, player=player)
    position = (getattr(init_node, player.lower()) - getattr(node, player.lower())).pop()
    new_position = (getattr(node, player.lower()) - getattr(init_node, player.lower())).pop()
    return node.parent.visits, (position, new_position)


if __name__ == '__main__':
    # node = monte_carlo_tree_search(Node(depth=6, current_player='Black', white={1,3,17}, black={7,21,23}), {}, time_limit=30)
    from cProfile import Profile
    from pstats import SortKey, Stats

    for _ in range(10):
        utils, move, played = mcts(player='Black', white={1, 3, 17}, black={7, 21, 23}, time_limit=30)
        print(move)
    # with Profile() as profile:
    #     utils, move, played = mcts(player='Black', white={1,3,17}, black={7,21,23}, time_limit=60)
    #     (
    #         Stats(profile)
    #         .strip_dirs()
    #         .sort_stats(SortKey.CUMULATIVE)
    #         .print_stats()
    #     )


