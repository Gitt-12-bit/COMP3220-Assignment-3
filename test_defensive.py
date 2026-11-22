#Checks that the defensive evaluation works with the search at depth 3. Expected output is a legal opening move
import chess
from move_search import choose_move
from agents.defensive import evaluate

board = chess.Board()
print(choose_move(board, 3, evaluate))