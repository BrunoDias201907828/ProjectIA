import arcade
from neutreeko import Neutreeko
from minmax import minimax
from minimax_prunning import minimax_pruning
from monte_carlo import mcts
import numpy as np
import argparse
import functools
from utils import eval_alignment, eval
eval_basic = functools.partial(eval, fn=None)


class NeutreekoAIvsAI(Neutreeko):
    algorithms_mapper = {
        'MinimaxPruning': minimax_pruning, 'Minimax': minimax, 'MonteCarlo': mcts,
        'Easy': functools.partial(minimax_pruning, depth=4, heuristic=eval_alignment),
        'Normal': functools.partial(minimax_pruning, depth=4, heuristic=eval_basic),
        'Difficult': functools.partial(minimax_pruning, depth=6, heuristic=eval_basic),
        'Expert': functools.partial(minimax_pruning, depth=8, heuristic=eval_basic)
    }

    def __init__(self, algorithm1: str, algorithm2: str, algorithm_index: int | None = None):
        super().__init__(name='Neutreeko - AI vs AI')
        self.algorithm_turn = None
        self.algorithm_names = {1: algorithm1, 2: algorithm2}
        self.algorithms = {i: self.algorithms_mapper[name] for i, name in self.algorithm_names.items()}
        self.init_algorithm_index = algorithm_index
        self.algorithm_index = None
        self.algorithm = None
        self.started = None
        self.display_running = None
        self.end_game_message_size = self.end_game_message_size // 2

    def setup(self):
        super().setup()
        self.algorithm_index = np.random.choice([1, 2]) if self.init_algorithm_index is None else self.init_algorithm_index
        self.started = False
        self.display_running = False

    def on_draw(self):
        super().on_draw()
        if self.started and not self.finished and self.display_running:
            text = f'{self.algorithm_names[self.algorithm_index]} is running...'
            arcade.draw_text(text, self.width - 250, 30, arcade.color.BLACK, 24, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.started = True
        if not self.finished:
            self.display_running = True
            self.on_draw()
            self.ai_move()
            self.display_running = False
            self.on_draw()
            self.change_algorithm()

    def change_algorithm(self):
        self.algorithm_index = 1 if self.algorithm_index == 2 else 2

    def ai_move(self):
        ai_fn = self.algorithms[self.algorithm_index]
        _, move, _ = ai_fn(set(self.get_white_positions()), set(self.get_black_positions()), self.turn,
                           played_moves=self.state_counter)
        self.selected_piece = [piece for piece in self.pieces if piece.square.number == move[0]][0]
        self.move_piece(self.squares[move[1]])
        self.change_turn()
        self.selected_piece = None
        self.maybe_finish_game()
        if self.finished:
            if 'draw' not in self.end_game_message.lower():
                self.end_game_message = f'{self.algorithm_names[self.algorithm_index]} Wins'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Neutreeko AI vs AI Game Mode')
    parser.add_argument('-a1', '--algorithm1', type=str, choices=['MinimaxPruning', 'Minimax', 'MonteCarlo'])
    parser.add_argument('-a2', '--algorithm2', type=str, choices=['MinimaxPruning', 'Minimax', 'MonteCarlo'])
    parser.add_argument('-i', '--init_algorithm_index', type=int, choices=[1, 2], default=None)
    args = parser.parse_args()
    game = NeutreekoAIvsAI(args.algorithm1, args.algorithm2, args.init_algorithm_index)
    game.setup()
    game.run()
