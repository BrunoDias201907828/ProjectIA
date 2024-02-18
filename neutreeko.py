from utils import *
import arcade
from pathlib import Path

# Screen title and size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Neutreeko"


class Valid(arcade.Sprite):
    def __init__(self, number, scale=.01):
        self.number = number
        self.path = Path(__file__).parent.joinpath('assets/green.png')
        super().__init__(str(self.path), scale,
                         center_x=375 + 130 * (number %  5),
                         center_y=790 - 130 * (number // 5))
        self.visible = False


class Square(arcade.Sprite):
    def __init__(self, number, scale=.15):
        self.number = number
        self.path = Path(__file__).parent.joinpath('assets/square.png')
        super().__init__(str(self.path), scale,
                         center_x=375 + 130 * (number %  5),
                         center_y=790 - 130 * (number // 5))


class Piece(arcade.Sprite):
    def __init__(self, square: Square, team: str):
        self.square = square
        self.team = team
        self.path = Path(__file__).parent.joinpath(f'assets/{self.team}.png')
        scale = {'black': .2, 'white': .25}[self.team]
        super().__init__(str(self.path), scale, center_x=self.square.center_x, center_y=self.square.center_y)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.turn = None
        self.selected_piece = None
        self.valid_squares = None
        self.pieces = None
        self.squares = None
        self.valid_squares_sprite = None
        self.state_counter = None
        self.finished = None
        self.end_game_message = None

        arcade.set_background_color(arcade.color.BABY_BLUE)

    def is_draw(self) -> bool:
        key = (frozenset(self.get_black_positions()), frozenset(self.get_white_positions()))
        new_value = self.state_counter.get(key, 0) + 1
        if new_value == 3:
            return True
        self.state_counter[key] = new_value
        return False

    def get_winner(self) -> str | None:
        if is_winner(self.get_black_positions()):
            return 'black'
        if is_winner(self.get_white_positions()):
            return 'white'

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.turn = 'black'
        self.finished = False
        self.end_game_message = None
        self.selected_piece = None
        self.valid_squares = None
        self.pieces = arcade.SpriteList()
        self.squares = arcade.SpriteList()
        self.valid_squares_sprite = arcade.SpriteList()
        self.state_counter = {}
        initial_black = (7, 21, 23)
        initial_white = (1, 3, 17)

        for i in range(25):
            self.squares.append(Square(i))
            self.valid_squares_sprite.append(Valid(i))
        for i in initial_black:
            self.pieces.append(Piece(self.squares[i], 'black'))
        for i in initial_white:
            self.pieces.append(Piece(self.squares[i], 'white'))
        self.is_draw()

    def on_draw(self):
        self.clear()
        self.squares.draw()
        self.pieces.draw()
        self.valid_squares_sprite.draw()
        if self.finished and self.end_game_message:
            arcade.draw_text(self.end_game_message, self.width // 2, self.height // 2, arcade.color.RED_BROWN,
                             font_size=96, anchor_x="center", bold=True)
        else:
            turn_text = f"{self.turn.capitalize()}'s Turn"
            arcade.draw_text(turn_text, self.width // 2, self.height - 50, arcade.color.BLACK, 24, anchor_x="center")

    def get_white_positions(self):
        return [p.square.number for p in self.pieces if p.team == 'white']

    def get_black_positions(self):
        return [p.square.number for p in self.pieces if p.team == 'black']

    def highlight_valid_squares(self):
        if self.valid_squares is not None:
            for square in self.valid_squares:
                self.valid_squares_sprite[square.number].visible = True

    def remove_highlights(self):
        if self.valid_squares is not None:
            for square in self.valid_squares_sprite:
                square.visible = False

    def change_turn(self):
        self.turn = 'white' if self.turn == 'black' else 'black'

    def finish_game(self, message):
        self.finished = True
        self.end_game_message = message

    def move_piece(self, square: Square):
        self.selected_piece.square = square
        self.selected_piece.center_x, self.selected_piece.center_y = square.center_x, square.center_y

    def get_valid_squares(self, piece) -> tuple[Square] | None:
        piece_number = piece.square.number
        pieces_numbers = {p.square.number for p in self.pieces}
        valid = [self.squares[i] for i in possible(piece_number, pieces_numbers)]
        if valid:
            return valid

    def on_mouse_press(self, x, y, button, key_modifiers):
        if not self.finished:
            piece = [p for p in arcade.get_sprites_at_point((x, y), self.pieces) if p.team == self.turn]
            if piece:
                self.remove_highlights()
                self.selected_piece = piece[0]
                self.valid_squares = self.get_valid_squares(piece[0])
                self.highlight_valid_squares()
            elif self.selected_piece is not None and self.valid_squares is not None:
                square = arcade.get_sprites_at_point((x, y), self.squares)
                if square and square[0] in self.valid_squares:
                    self.move_piece(square[0])
                    self.change_turn()

                    draw = self.is_draw()
                    winner = self.get_winner()
                    if draw:
                        self.finish_game('Draw')
                    if winner is not None:
                        self.finish_game(f'Winner: {winner}')

                self.selected_piece = None
                self.remove_highlights()

            else:
                self.selected_piece = None
                self.remove_highlights()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.setup()


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()