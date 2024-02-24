import math
import random
import time
from utils import *

class mctsNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

class GameState:
    def __init__(self, white_positions=None, black_positions=None, player = None, position_history=0):
        self.current_player = player
        self.white_positions = white_positions or set()
        self.black_positions = black_positions or set()
        self.position_history = position_history
    
    def is_draw(self, position_history):
        current_position = hash(tuple(sorted(self.white_positions))) + hash(tuple(sorted(self.black_positions)))

        if current_position in position_history:
            position_history[current_position] += 1
            return position_history[current_position] == 3
        else:
            position_history[current_position] = 1
            return False


def monte_carlo_tree_search(root_node):
    start_time = time.time()

    while resources_left(start_time, computational_power): #needs implementing space limit
        leaf = traverse(root_node)
        sim_result=rollout(leaf)
        backpropagate(leaf, sim_result)
    return best_child(root_node)

def resources_left(start_time, time_limit): #needs implementing time_limit
    time_limit=30
    return time.time() - start_time < time_limit


#function for node traversal
def traverse(node):
    while fully_expanded(node):
        node=best_uct(node)

        #in case no children are present/ node is terminal
    return pick_unvisited(node.children) or node

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
def rollout(node):
    while not is_terminal(node): 
        node = rollout_policy(node)
        return result(node)
    
def result(node):

    if is_winner(node.state, 'Black'):
        return 1  # Black wins
    elif is_winner(node.state, 'White'):
        return -1  # White wins
    elif node.state.is_draw(node.state.position_history): #check this line
        return -0.2  # Draw
    else:
        # Handle other cases if needed
        return 0  # Default case, no result
    
def is_terminal(node): #is_winner get from utils
    return is_winner('Black') or is_winner('White') or node.state.is_draw(node.state.position_history)

    
#function for randomly selecing a child node
def rollout_policy(node):
    return pick_random(node.children)

#pick a random child
def pick_random(children):
    return random.choice(children)


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

def best_uct(node, exploration_factor=1.41):
    if not node.children:
        return None  # No children to choose from

    # UCT formula: uct_value = win_rate/visits + exploration_factor * sqrt(log(total_visits)/visits)
    uct_values = [
        (child.wins / child.visits) + exploration_factor * math.sqrt(math.log(node.visits) / child.visits)
        for child in node.children
    ]

    best_child = node.children[uct_values.index(max(uct_values))]
    return best_child