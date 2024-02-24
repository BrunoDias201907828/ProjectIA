import math
import random
import time
from utils import *
from utils_mcts import *
from monte_carlo_node import *

def resources_left(start_time, time_limit):
    return time.time() - start_time < time_limit

def monte_carlo_tree_search(root_node, played_moves, time_limit=30):
    start_time = time.time()
    cur_node = root_node
    while resources_left(start_time, time_limit): #ou entao por numero de simulaçoes
        
        for position, moves in possible_moves(cur_node):
            for new_position in moves:
                child = perform_action_mcts(cur_node, position, new_position)
                cur_node.add_child(child)

        leaf = traverse(cur_node)
        sim_result=rollout(leaf, played_moves)
        backpropagate(leaf, sim_result)
    return best_child(root_node)

#function for node traversal
def traverse(node):
    while len(node.children) != 0:
        node=best_uct(node)

        #in case no children are present/ node is terminal
    return pick_unvisited(node.children) or node

#check for children -- is it fully expanded?
def fully_expanded(node):
    if len(node.children) == 0:    
        return False  # No children to expand

    # Check if all children have been expanded
    return all(child.visits > 0 for child in node.children)

def best_uct(node, exploration_factor=1.41):

    # UCT formula: uct_value = win_rate/visits + exploration_factor * sqrt(log(total_visits)/visits)
    uct_values = [
        (child.wins / child.visits) + exploration_factor * math.sqrt(math.log(node.visits) / child.visits)
        for child in node.children
    ]

    best_child = node.children[uct_values.index(max(uct_values))]
    return best_child

#pick an unvisited node
def pick_unvisited(children):
    unvisited_children = [child for child in children if child.visits == 0]
    return random.choice(unvisited_children) if unvisited_children else None

#check for children -- is it fully expanded?
def fully_expanded(node):
    if not node.children:
        return False  # No children to expand

    # Check if all children have been expanded
    return all(child.visits > 0 for child in node.children)

#function for the result of the simulation
def rollout(node, played_moves):
    while not is_terminal(node, played_moves, first=True):
        node = random.choice(node.children)
        #implementar resultado (utility function)
    return result(node)

#function for backpropagation
def backpropagate(node, result):
    if node.parent is None:
        return
    #update the stats
    node.visits += 1
    node.wins += result
    backpropagate(node.parent, result)

#function for selecting the best child
#node with highest number of visits
def best_child(node):
    if not node.children:
        return None  # No children to choose from

    best_child = max(node.children, key=lambda child: child.visits)
    return best_child
