import math
import random
import time
from utils import possible_moves, update_played_moves
from utils_mcts import *
from monte_carlo_node import *

def resources_left(start_time, time_limit):
    return time.time() - start_time < time_limit

def monte_carlo_tree_search(root_node, played_moves, time_limit=10, selection_depth=3, player='Black'):
    start_time = time.time()
    root_node.depth = selection_depth
    expand_node(root_node)

    while resources_left(start_time, time_limit): #ou entao por numero de simulaçoes
        leaf = traverse(root_node)
        sim_result=rollout(leaf, played_moves, player)
        backpropagate(leaf, sim_result)
    return best_child(root_node)


def expand_node(node):
    if node.depth > 0:
        for position, moves in possible_moves(node):
            for new_position in moves:
                child = perform_action_mcts(node, position, new_position)
                node.add_child(child)
                expand_node(child)
            
#function for node traversal
def traverse(node):
    while fully_expanded(node):
        node=best_uct(node)

        #in case no children are present/ node is terminal
    return pick_unvisited(node.children) or node

#check for children -- is it fully expanded?
def fully_expanded(node):
    if len(node.children) == 0:
        return False  # No children to expand

    # Check if all children have been expanded
    return all(child.visits > 0 for child in node.children)


def uct(node, child):
    if child.visits == 0:
        return math.inf
    #try:
    return (child.utility / child.visits) + math.sqrt(2*math.log(node.visits) / child.visits)
    #except:
    #   from IPython import embed; embed()

def best_uct(node):
    uct_values = [uct(node, child) for child in node.children]

    best_child = node.children[uct_values.index(max(uct_values))]
    return best_child

#pick an unvisited node
def pick_unvisited(children):
    unvisited_children = [child for child in children if child.visits == 0]
    return random.choice(unvisited_children) if unvisited_children else None

#function for the result of the simulation
def rollout(node, played_moves, player):
    while not is_terminal(node, played_moves, first=False):
        position, moves = random.choice(possible_moves(node))
        move = random.choice(moves)
        node = perform_action_mcts(node, position, move)

    return result(node, player)

def result(node, player):
    if is_winner(getattr(node, player.lower())):
        return 1
    if is_winner(getattr(node, 'white' if player.lower() == 'black' else 'black')):
        return 0
    
    return 0.5

#function for backpropagation
def backpropagate(node, result):
    if node is None:
        return
    #update the stats
    node.visits += 1
    node.utility += result
    backpropagate(node.parent, result)

#function for selecting the best child
#node with highest number of visits
def best_child(node):
    print(node.black, node.white)
    best_child = max(node.children, key=lambda child: child.visits)
    return best_child

@update_played_moves
def mcts(white: set, black: set, player: str, played_moves: dict | None = None, selection_depth: int = 4, time_limit: int = 10):
    init_node = Node(depth=selection_depth, current_player=player, white=white, black=black)
    node = monte_carlo_tree_search(init_node, played_moves, time_limit=time_limit, selection_depth=selection_depth, player=player)
    print([child.visits for child in init_node.children])
    position = init_node.black - node.black
    pos = position.pop()
    new_position = node.black - init_node.black
    new_pos = new_position.pop()
    move = (pos, new_pos)

    return node.utility, move

if __name__ == '__main__':
    #node = monte_carlo_tree_search(Node(depth=6, current_player='Black', white={1,3,17}, black={7,21,23}), {}, time_limit=30)
    utils, move, played = mcts(player='Black', white={1,3,17}, black={7,21,23}, time_limit=30)
    print(utils)
    print(move)
    print(played)

