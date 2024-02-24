from utils import *
import math


class MCTSNode:
    def __init__(self, current_player='Black', white={1, 3, 17}, black={7, 21, 23}, repetition=1, parent=None):
        self.white = white
        self.black = black
        self.current_player = current_player
        self.repetition = repetition
        self.children = {}
        self.parent= parent
        self.visit_count = 1
        self.win_score = 0
    
    #def repeated_state(self):
        #"""Checks if state has been repeated 3 times"""
        #self.parent.visit_count += 1
      
        #return
        #def is_draw(self):
          #if self.parent.visit_count >=3:
            #return True
        #return False
    
    
    def is_terminal(self):
        """Checks whether there is a winner"""
        return is_winner(self.black) or is_winner(self.white) or self.repetition >= 3 #checks if there is a win or a draw
    
    def get_state(self):
        """Returns the state of the game"""
        return self.current_player, self.white, self.black
    
   
    def add_child(self, action, child_node):
        """Add a child to the root node"""
        self.children[action] = child_node

    def increment_visit_count(self):
        """adds to the visit count of the node"""
        self.visit_count += 1

    def update_win_score(self, score): #should this be like +1 0 and -1? Check score function in game!
        """Updates the win score"""
        self.win_score += score
       
    def get_action(self, mcts_node: 'MCTSNode') -> list[tuple[int, int]]: #start position of piece, end position of piece
        """Retrieve available moves from the given MCTS node."""
        current_player = mcts_node.current_player
        if current_player == 'Black':
            player_positions = mcts_node.black
        else:
            player_positions = mcts_node.white
        
        available_moves = []
        for position in player_positions:
            moves = possible_moves(position, mcts_node.black | mcts_node.white)
            available_moves.extend([(position, move) for move in moves])
        
        return available_moves

    #get_action may return me for example:
    # available_moves = [
    #(7, 10), (7, 14),  # Piece at position 7
    #(21, 17), (21, 18), (21, 22),  # Piece at position 21
    #(23, 19)  # Piece at position 23
    #]
    