from .utils import is_draw, is_winner, get_repetitions, possible_moves
import math


class Node:
    def __init__(self, current_player='Black', repetition=1, white=None, black=None, parent=None):
        if white is None:
            white = {1, 3, 17}
        if black is None:
            black = {7, 21, 23}
        self.white = white
        self.black = black
        self.repetition = repetition
        self.current_player = current_player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.utility = 0
        self._is_terminal = None
        self._is_winner = {}

    def add_child(self, child):
        self.children.append(child)

    def create_children(self):
        for position, new_positions in possible_moves(self):
            for new_position in new_positions:
                child = perform_action_mcts(self, position, new_position)
                self.add_child(child)

    @property
    def uct(self):
        if self.visits == 0:
            return math.inf
        return self.utility / self.visits + (2 * math.log(self.parent.visits) / self.visits) ** 0.5

    def is_terminal(self, played_moves):
        if self._is_terminal is None:
            self._is_terminal = is_terminal(self, played_moves)
        return self._is_terminal

    def is_winner(self, player):
        if player in self._is_winner:
            return self._is_winner[player]
        value = is_winner(getattr(self, player.lower()))
        self._is_winner[player] = value
        return value

    def remove_terminal_children(self, played_moves):
        self.children = [child for child in self.children if not child.is_terminal(played_moves)]


def perform_action_mcts(node, position, new_position):
    player = node.current_player.lower()
    new_positions = getattr(node, player).copy()
    new_positions.remove(position)
    new_positions.add(new_position)
    repetition = get_repetitions(node)
    if player == 'black':
        return Node(white=node.white.copy(), black=new_positions, current_player='White',
                    repetition=repetition, parent=node)
    else:
        return Node(white=new_positions, black=node.black.copy(), current_player='Black',
                    repetition=repetition, parent=node)


def is_terminal(node, played_moves):
    win_lose_condition = any([is_winner(node.black), is_winner(node.white)])
    draw_condition = is_draw(node, played_moves)
    return win_lose_condition or draw_condition

