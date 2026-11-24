#ID NUMBERS: 620171757, 620160983
#Checks that the defensive evaluation works with the search at depth 3. Expected output is a legal opening move
import chess
from move_search import choose_move
from agents.defensive import evaluate

board = chess.Board()
move = choose_move(board, 3, evaluate)
print("test defensive:", "PASS" if move in board.legal_moves else "FAIL", "- choose", move)