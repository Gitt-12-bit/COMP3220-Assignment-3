#ID NUMBERS: 620171757, 620160983
#Sanity checks for attacking evaluation. Expected: starting position scores 0, and a position and its colour-mirrored copy
#score the same size with opposite signs (for example 61 and -61)
import chess
from agents import attacking

start = attacking.evaluate(chess.Board())
board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
score, mirrored = attacking.evaluate(board), attacking.evaluate(board.mirror())
print("test attacking:", "PASS" if start == 0 and score == -mirrored else "FAIL", "- start", start, "| position", score, "| mirrored", mirrored)