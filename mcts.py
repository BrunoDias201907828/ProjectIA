from node import Node
from utils import *
import math

#Let's define the state as the positions of the pieces at a given move.
#Let's define the possible actions as the set of moves which are available to
#P_a(s,s')—is the transition function modelled by a probability that action -a- is performed in state -s- will lead to -s′-
#the above probability in this case is 1
#Ra(s)—is the immediate reward (payof) for reaching state s by action a. In Markov 
#games, where states incorporate all the necessary information (that summarizes the history), the action component can be omitted

#MCTS is allotted some computational budget which can be either specifed by the number of iterations or the time available for making a decision
#a∗ = arg max_a∈A(s) of Q(s, a)
#_ means subscrpit. in this case all the possible decisions belong to space A(s) - all the possible actions available at that state
#Q(s, a) denotes the empirical average result of playing action a in state s
# to this maximizing function we can also add an exploration term such as: exploration_factor*log(N(s))/N(s)
#this exploration_factor can be seen as a bias, that can change over time. Progressive_bias = W* H_i/(T_i(1 − X̄_i) + 1
# H_i is the heuristic value, X̄_i is the average reward for the node, T_i is the number of node visits and W is a positive constant controlling the impact of the bias
# We may also only want to consider if it's over a certain number and discount it (=set to 0) as to not explore that node
class MCTS_node():
    def __init__(self, current_player='Black', white={1, 3, 17}, black={7, 21, 23}, sims=100):
        self.white = white
        self.black = black
        self.current_player = current_player
        self.simulations = sims
class MCTS():
    def __init__(self, current_player = 'Black', white = {1,3,17}, black = {7,21,23}, sims=100):
        self.white = white
        self.black = black
        self.current_player = current_player
        self.simulations = sims # number of simultaions
        self.wins = 0
        self.visits = 0
        self.root_node = MCTS_node(current_player=current_player, white=white, black=black)
        self.parent = None
        self.children = {} # implementing as a dictionary due to sparcebranching (many possible actions lead to the same game state)
        self.visit_counts = {}  # Dictionary to store visit count for each child node
        self.cache_size = 10000 #is this a good number?
        self.cache = {}

    def is_terminal(self, node):
        # Check if the node is a terminal state
        return any([is_winner(node.black), is_winner(node.white)]) or node.repetition >= 3 or node.depth == 0

    def get_move_from_node(self, parent_node, child_node):
        # Retrieve the move associated with the child node from the parent node
        for move, node in parent_node.children.items():
            if node == child_node:
                return move
        return None  # Return None if the child node is not found in the parent's children

    def cache_sub_tree(self, node):
        # Cache sub-tree rooted at the given node
        if len(self.cache) >= self.cache_size:
            self.manage_cache()
        self.cache[node] = node

    def retrieve_cached_sub_tree(self, node):
        # Retrieve a cached sub-tree if it matches the given node
        return self.cache.get(node, None)

    def manage_cache(self):
        # Manage the size of the cache to prevent it from growing too large
        if len(self.cache) > self.cache_size:
            # Remove the least recently used nodes from the cache
            self.cache.popitem()
    
    #action/available_legal_moves
    def add_child(self, action, child_node): #EXPANSION
        self.children[action] = child_node
        self.visit_counts[action] = 0  # Initialize visit count to 0 for the new child node

    def increment_visit_count(self, action):
        self.visit_counts[action] += 1
    
    @staticmethod
    def select_child_ucb(node, exploration_factor): #SELECTION
        """Select a child node based on the Upper Confidence Boundary formula."""
        selected_child = None
        best_ucb_value = -float('inf')

        for child in node.children:
            if child.visits == 0:
                return child  # Choose unvisited child 
            else:
                ucb_value = (child.wins / child.visits) + exploration_factor * math.sqrt(
                    math.log(node.visits) / child.visits
                )
                if ucb_value > best_ucb_value:
                    selected_child = child
                    best_ucb_value = ucb_value

        return selected_child
    def is_terminal(self, node):
        return any([is_winner(node.black), is_winner(node.white)]) or node.repetition >= 3 or node.depth == 0
    
    def backpropagate(self, node, result):
        """Backpropagate the result of a simulation up the tree."""
        while node is not None:
            node.visits += 1
            if result == node.current_player:  # Assuming result is either 'Black' or 'White'
                node.wins += 1
            node = node.parent  # Move up to the parent node

    def search(self, root_node):
        """Perform Monte Carlo Tree Search starting from the root node."""
        for _ in range(self.simulations):
            selected_node = root_node
            while not self.is_terminal(selected_node):
                if not selected_node.children:
                    self.expand(selected_node)
                selected_node = self.select_child_ucb(selected_node, exploration_factor=1.0)
            simulation_result = self.simulate(selected_node)
            self.backpropagate(selected_node, simulation_result)
        # After all simulations, return the best move and its value from the root node
        best_child = max(root_node.children.values(), key=lambda x: x.visits)
        best_value = best_child.wins / best_child.visits if best_child.visits > 0 else 0
        return best_value, best_child
    
   

    def get_move_from_node(parent_node, child_node):
    # Your implementation depends on how moves are represented in your game and stored in the nodes.
    # Assuming that moves are stored as tuples (position, new_position), you can do something like this:
        for move, node in parent_node.children.items():
            if node == child_node:
                return move
        return None  # Return None if the child node is not found in the parent's children

    def run(self, current_player, white_positions, black_positions, depth):
        """Run the Monte Carlo Tree Search algorithm."""
        root_node = self.create_root_node(current_player, white_positions, black_positions, depth)
        best_value, best_child = self.search(root_node)
        best_move = self.get_move_from_node(root_node, best_child)
        return best_value, best_move
    

def mcts_search(depth, current_player, white, black, simulations):
    mcts = MCTS(current_player=current_player, white=white, black=black, sims=simulations)
    best_value, best_move = mcts.run(depth)
    return best_value, best_move
# Example usage:
best_value, best_move = mcts_search(5, 'Black', {1, 3, 17}, {7, 21, 23}, simulations=1000)
print("Best value:", best_value)
print("Best move:", best_move)