import random
import chess

class RefAgent:
    def __init__(self):
        self.name = "Reference"
        self.level = "n/a"
        self.depth = 0

    def set_difficulty(self, level):
        pass

    def get_move(self, board):
        moveslegal = list(board.legal_moves)
        return random.choice(moveslegal) if moveslegal else None