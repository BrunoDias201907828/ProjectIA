from mcts_node import *
import random 
import time
from copy import deepcopy

def montecarlo_treesearch(white: set, black: set, player: str, simulations: int=6):
    root_node = MCTSNode(white=white, black=black, current_player=player, repetition=1)
    mcts_move=MCTS(root_node,exploration_factor=0.2,simulations=simulations,mcts_player=player)
    return mcts_move.get_best_child()

class MCTS:
    def __init__(self, root_node, exploration_factor=0.2, simulations=10, mcts_player = 'White'):
        """
        Initialize the MCTS algorithm with a root node and exploration factor.

        Args:
            root_node (MCTSNode): The root node of the search tree.
            exploration_factor (float): The exploration factor used in UCB selection.
        """
        self.root_node = root_node
        self.exploration_factor = exploration_factor
        self.simulations=simulations
        self.branch =[]
        self.mcts_player = mcts_player
        
    def opposite_player(self):
        """
        Can work as a switch player method or as an identifier
        for example calling this on self.mcts_player will switch it, calling it on it's own will identify opponent
        """
        return 'White' if self.mcts_player == 'Black' else 'Black'
    
    @staticmethod
    def select_child_ucb(node, exploration_factor): #Selection criteria/ what nodes to expand look
        """
        Select a child node based on the Upper Confidence Bound (UCB) formula.
        It's going to evaluate the child nodes based on potential for expansion

        Args:
            node (MCTSNode): The parent node from which to select a child.
            exploration_factor (float): The exploration factor used in UCB selection.

        Returns:
            MCTSNode: The selected child node.
        """
        selected_child = None
        best_ucb_value = -float('inf')

        for child in node.children:
            if child.visit_count == 0:
                return child  # Choose unvisited child 
            else:
                ucb_value = (child.wins / child.visit_count) + exploration_factor * math.sqrt(
                    math.log(node.visit_count) / child.visit_count
                )
                if ucb_value > best_ucb_value:
                    selected_child = child
                    best_ucb_value = ucb_value

        return selected_child # the child selected is a position, i.e. a gamestate
    
    def get_best_child(self):
        """
        Return the child node with the highest win rate.

        Args:
            node (MCTSNode): The parent node to select the best child from.

        Returns:
            MCTSNode: The best child node.
        """
        # Return the child node with the highest utility score, in this case win rate
        result = max(self.root_node.children.values(), key=lambda x: x.win_score / x.visit_count)
        #if winning_line_True(root_node):
            #result = winning_line(root_node)
        return result


    def random_action(self, node):
        """Do a Random move"""
        actions=[]
        for action in node.get_actions():
            actions.append(action)
        random_action = random.choice(actions)
        return random_action # a random action that will give rise to a new state. Doesn't perform the action!!
    
    def expand_all(self, node):
        """
        Expand the search tree by creating child nodes for all possible actions 
        - node.get_actions is a list of all legal moves all pieces can do
        
        Args:
            node (MCTSNode): The node to expand.
        """
        # Create a child nodes for each of the  states that arise from the possible actions a piece can make and adds to children
        for action in node.get_actions():
            child_node = self.perform_action(node, action)
            node.add_child(action, child_node)
            
    def expand_random(self,node):
        """
        Expand the search tree by creating child nodes for a random action

        Args:
            node (_type_): _description_
            random_action (_type_): _description_
        """
        # Create a child nodes for a random chosen state that arises from the possible actions a piece can make
        action = self.random_action(node)
        child_node = self.perform_action(node, action)
        node.add_child(action, child_node)
    
    def perform_action(self,node, action) -> 'MCTSNode':
        """
        Apply the specified action to the given node's game state and return the resulting child node/gamestate.

        Args:
            node (MCTSNode): The node whose game state to update.
            action: The action to apply to the game state. Selected by some criteria from node.get_action

        Returns:
            MCTSNode: The new child node representing the game state after applying the action.
        """
        # Make a copy of the node and get the current game state
        copy_node = node.copy()
        current_player,copy_white, copy_black = copy_node.get_state()

        # Update the game state based on the action
        piece, new_piece = action
        if current_player == 'Black':
            copy_black.add(current_player, piece, new_piece) #remove that piece from the set -- THESE METHODS NEED TO BE ADDED
                 
            current_player = 'White' #switch
        else:
            copy_white.add(current_player, piece, new_piece) #remove that piece from the set -- THESE METHODS NEED TO BE ADDED
            
            current_player = 'Black'

        child = MCTSNode(current_player=current_player, white=copy_white, black=copy_black, repetition=node.repetition, parent=node)

        # Create and return a new child node with the updated game state
        return child
        
    def add(piece_colour, node): #maybe call it substitute?
        if current_player == 'Black':
            return node.black = set()
        else:
            return node.white = set()
        

    def run_simulations(self, node):
        """
        Run random simulations from the given node until reaching a terminal state.
        Using random_actions

        Args:
            node (MCTSNode): The node to start the simulations from.
        """
        while not node.is_terminal():
            # Perform a random action
            action = self.random_action(node)
            child_node = self.perform_action(node, action)    
        return child_node #this child node is a terminal node
    
    def simulate(self, node, simulations):
        """
        Simulate the game from the current node until the end and return the result (e.g., win/loss) currently using random moves.
        
        Args:
            node (MCTSNode): The node to start the simulation from.
            simulations (int): The number of random simulations to run from the current node.

        Returns:
            float: The result of the simulation (e.g., 1.0 for win, 0.0 for draw, -1.0 for loss).
        """
        for _ in range(simulations):
            current_node = node.deepcopy()  # Make a copy of the current node for simulation
            #Should I use deepcopy or is clone() enough?
            
            # Run random simulations until reaching a terminal state
            end_node=self.run_simulations(current_node)
            
            
            if is_winner(self.mcts_player):
                return 1.0  # Current player wins
            elif is_winner(self.opposite_player):
                return -1.0  # Opponent wins
            else:
                return 0.0  # Draw


    def backpropagate(self, node, result):
        """
        Update visit count and win score of nodes along the path from the current node to the root.

        Args:
            node (MCTSNode): The node to start backpropagation from.
            result (float): The result of the simulation to propagate up the tree.
        """
        # Update visit count and win score of nodes
        # along the path from the current node to the root
        while node is not None:
            node.visit_count += 1
            node.win_score += result
            node = node.parent
        for node in reversed(self.branch):
            node.visit_count += 1
            node.win_score += result
    
    #This is the main loop:
    def search(self, iterations):
        """
        Perform MCTS search for a specified number of iterations. 
        This is the main loop. 
        After generating all possible direct-children/Neighbour we select one either by random or through a criteria.
        We then simulate it until we reach a final position (by random choices of its children) - either win, loss or draw using the simulate method 
        After the simulation, the result is backpropagated up the tree. The visit counts and the win scores (or values) of 
        nodes traversed during the selection phase are updated based on the result of the simulation.
        We Repeat This process n times (iterations)
        Finally we call on the select best child method that has been keeping track of the best child node - direct-child/neighbour 
        
        
        Args:
            iterations (int): The number of iterations to perform the search.

        Returns:
            MCTSNode: The best child node found after the search.
        """
        for _ in range(iterations):
            node = self.root_node
            
            # Selection phase
            while not node.is_terminal():
                # Expand if necessary -- see all the children
                if not node.children:
                    # (Create child nodes for all possible actions)
                    self.expand_all(node) 
                    # We could use self.expand_random(node) to choose randomly,
                    # or a method such as self.expand_heuristic() to choose through some other heuristic
                    self.run_simulations(node)
                # Select child node using UCB
                most_promising_node = self.select_child_ucb(node=node,exploration_factor=self.exploration_factor)
                
            # Simulation phase
            result = self.run_simulations(most_promising_node)
            
            # Backpropagation phase
            self.backpropagate(node, result)
        
        # Return the best child of the root node
        return self.get_best_child(self.root_node)
    
if __name__ == '__main__':
    t0 = time.time()
    value, move = montecarlo_treesearch({1, 3, 17}, {7, 21, 23}, 'Black', depth=6)
    print(time.time() - t0)
    print(value, move)