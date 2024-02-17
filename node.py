class Node:
    def __init__(self, depth, current_player = 'Black', repetition = 1, white = {1,3,17}, black = {7,21,23}):
        self.white = white
        self.black = black
        self.repetition = repetition
        self.depth = depth
        self.current_player = current_player