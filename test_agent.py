import chess
from agents.base_agent import Agent
from agents.defensive import evaluate

agent = Agent("Defensive", evaluate, depth=3)
board = chess.Board()
print(agent.name, agent.choose_move(board))