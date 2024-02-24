class Node:
    def __init__(self, current_player = 'Black', repetition = 1, white = {1,3,17}, black = {7,21,23}, parent=None):
        self.white = white
        self.black = black
        self.repetition = repetition
        self.current_player = current_player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child):
        self.children.append(child)