from neutreeko import Neutreeko
from minmax import minimax
from alpha_beta import minimax_pruning
from monte_carlo import mcts
import arcade
import random
import argparse
import functools
from utils import eval_alignment, eval
eval_basic = functools.partial(eval, fn=None)


class NeutreekoAI(Neutreeko):
    def __init__(self, mode: str = 'minimax_pruning', start_ai: bool = None):
        super().__init__(name='Neutreeko - Human vs AI')
        self.start_ai = start_ai
        self.ai_turn = None
        self.mode = mode
        self.ai_fn = {
            'MinimaxPruning': minimax_pruning, 'Minimax': minimax, 'MonteCarlo': mcts,
            'Easy': functools.partial(minimax_pruning, depth=4, heuristic=eval_alignment),
            'Normal': functools.partial(minimax_pruning, depth=4, heuristic=eval_basic),
            'Difficult': functools.partial(minimax_pruning, depth=6, heuristic=eval_basic),
            'Expert': functools.partial(minimax_pruning, depth=8, heuristic=eval_basic)
        }[mode]
        self.ai_running = None

    def setup(self):
        super().setup()
        self.ai_turn = random.choice([True, False]) if self.start_ai is None else self.start_ai
        self.ai_running = False

    def on_draw(self):
        super().on_draw()
        text = "AI is running..."
        if self.ai_running:
            arcade.draw_text(text, self.width - 150, 50, arcade.color.BLACK, 24, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, x, y, button, key_modifiers) -> None:
        if self.ai_turn:
            self.ai_move()
        self.ai_turn = super().on_mouse_press(x, y, button, key_modifiers)
        self.on_draw()
        if not self.finished:
            if self.ai_turn:
                self.ai_move()

    def ai_move(self):
        self.ai_running = True
        turn_text = f"{self.turn.capitalize()}'s Turn"
        arcade.draw_text(turn_text, self.width // 2, self.height - 50, arcade.color.BLACK, 24, anchor_x="center")
        self.on_draw()
        _, move, _ = self.ai_fn(set(self.get_white_positions()), set(self.get_black_positions()), self.turn,
                                played_moves=self.state_counter)
        self.selected_piece = [piece for piece in self.pieces if piece.square.number == move[0]][0]
        self.move_piece(self.squares[move[1]])
        self.change_turn()
        self.ai_turn = False
        self.selected_piece = None
        self.maybe_finish_game()
        self.ai_running = False
        self.on_draw()


def main():
    parser = argparse.ArgumentParser(description='Neutreeko AI Game Mode')
    parser.add_argument('-m', '--mode'    , type=str , default='minimax_pruning')
    parser.add_argument('-s', '--start_ai', type=int, default=None)
    args = parser.parse_args()
    window = NeutreekoAI(mode=args.mode, start_ai=bool(args.start_ai) if args.start_ai is not None else None)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

