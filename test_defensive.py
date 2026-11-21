import chess
from move_search import choose_move
from agents.defensive import evaluate

board = chess.Board()
print(choose_move(board, 3, evaluate))