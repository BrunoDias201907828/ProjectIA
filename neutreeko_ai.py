from neutreeko import MyGame
from minmax import minimax_experimental
import arcade
import random


class NeutreekoAI(MyGame):
    def __init__(self):
        super().__init__()
        self.ai_turn = None

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
        _, move = minimax_experimental(set(self.get_white_positions()), set(self.get_black_positions()), self.turn, 3)
        self.selected_piece = [piece for piece in self.pieces if piece.square.number == move[0]][0]
        self.move_piece(self.squares[move[1]])
        self.change_turn()
        self.ai_turn = False
        self.selected_piece = None
        self.maybe_finish_game()


def main():
    window = NeutreekoAI()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
