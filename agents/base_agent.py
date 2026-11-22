import random
from move_search import choose_move as search_move

DIFFICULTY = {  "Easy": {"depth": 1, "blunder": 0.30}, 
                "Medium": {"depth": 2, "blunder": 0.05},
                "Hard": {"depth": 3, "blunder": 0.0},
                "Expert": {"depth": 4, "blunder": 0.0}
            }

#An agent is a name, an evaluation function and a search depth. Both the attacking and defensive agents use this same class.
class Agent:
    def __init__(self, name, evaluate, level="Medium"):
        #Initializes agent characteristics
        self.name = name
        self.evaluate = evaluate
        self.set_difficulty(level)

    #Set how far ahead agent seacrhes and the frequency of playing random moves
    def set_difficulty(self, level):
        """The GUI menu calls this function, for setting the difficulty. It accepts a level name or plain depth number."""
        if isinstance(level, int):
            self.level, self.depth, self.blunder_chance = f"Depth {level}", level, 0.0
            return
        settings = DIFFICULTY[level]
        self.level = level
        self.depth = settings["depth"]
        self.blunder_chance = settings["blunder"]

    #Returns the move the agent wishes to play. On Easy it sometimes plays a random legal move; otherwise it runs the alpha-beta search.
    #It searches a copy of the board so the real board is never changed.
    def choose_move(self, board):
        # copy so the real board is never touched
        legal_m = list(board.legal_moves)
        if not legal_m:
            return None
        if random.random() < self.blunder_chance:
            return random.choice(legal_m)
        return search_move(board.copy(), self.depth, self.evaluate)

    #Same as choose_move; this is the name the match harness uses.
    def get_move(self, board):   # name used by matches.py and GUI
        return self.choose_move(board)