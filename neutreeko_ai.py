from neutreeko import Neutreeko
from minmax import minimax
from minimax_prunning import minimax_pruning
from mcts2 import montecarlo_treesearch
import arcade
import random
import argparse


class NeutreekoAI(Neutreeko):
    def __init__(self, mode: str = 'minimax_pruning'):
        super().__init__(name='Neutreeko - Human vs AI')
        self.ai_turn = None
        self.mode = mode
        self.ai_fn = {'minimax_pruning': minimax_pruning, 'minimax': minimax}[mode]

    def setup(self):
        super().setup()
        self.ai_turn = random.choice([True, False])

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        if self.ai_turn:
            self.ai_move()
        self.ai_turn = super().on_mouse_press(x, y, button, key_modifiers)
        if self.ai_turn:
            self.ai_move()

    def ai_move(self):
        print("thinking...")
        _, move, _ = self.ai_fn(set(self.get_white_positions()), set(self.get_black_positions()), self.turn,
                                played_moves=self.state_counter)
        self.selected_piece = [piece for piece in self.pieces if piece.square.number == move[0]][0]
        self.move_piece(self.squares[move[1]])
        self.change_turn()
        self.ai_turn = False
        self.selected_piece = None
        self.maybe_finish_game()
        print("done")


def main():
    parser = argparse.ArgumentParser(description='Neutreeko AI Game Mode')
    parser.add_argument('-m', '--mode', type=str, default='minimax_pruning',
                        choices=['minimax_pruning', 'minimax', 'mcts'],
                        help='AI mode (minimax_pruning or minimax or monte_carlo_tree_search)')

    args = parser.parse_args()
    window = NeutreekoAI(mode=args.mode)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
