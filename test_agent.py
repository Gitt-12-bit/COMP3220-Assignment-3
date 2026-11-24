#ID NUMBERS: 620171757, 620160983
#Check that an Agent can be built and choose a legal opening move
import chess
from agents.base_agent import Agent
from agents import attacking, defensive

for name, evaluate in (("Attacking", attacking.evaluate), ("Defensive", defensive.evaluate)):
    agent = Agent(name, evaluate, 3)
    board = chess.Board()
    move = agent.choose_move(board)
    print("test agent:", "PASS" if move in board.legal_moves else "FAIL", "-", agent.name, "choose", move)