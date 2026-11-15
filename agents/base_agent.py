from move_search import choose_move as search_move

class Agent:
    def __init__(self, name, evaluate, depth=3):
        self.name = name
        self.evaluate = evaluate
        self.depth = depth
        
        

    def choose_move(self, board):
        #copy the board so the real one is never touched:
        work_board = board.copy()
        
        return search_move(work_board, self.depth, self.evaluate)
        