import random
import chess

class RefAgent:
    def __init__(self):
        #Initializes Reference agent
        self.name = "Reference"
        self.level = "n/a"
        self.depth = 0

    def set_difficulty(self, level):
        #Has no difficulty
        pass

    def get_move(self, board):
        #Gives the move for the reference agent to play
        moveslegal = list(board.legal_moves)
        return random.choice(moveslegal) if moveslegal else None