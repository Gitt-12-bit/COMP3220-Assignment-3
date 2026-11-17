from move_search import choose_move as search_move

DIFFICULTY = {"Easy": 1, "Medium": 2, "Hard": 3}

class Agent:
    def __init__(self, name, evaluate, level="Medium"):
        self.name = name
        self.evaluate = evaluate
        self.depth = DIFFICULTY[level] if isinstance(level, str) else level

    def choose_move(self, board):
        # copy so the real board is never touched
        return search_move(board.copy(), self.depth, self.evaluate)

    def get_move(self, board):   # name used by matches.py
        return self.choose_move(board)