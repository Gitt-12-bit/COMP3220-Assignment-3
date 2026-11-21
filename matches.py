import argparse
import os
import chess
from datetime import datetime

from agents.base_agent import Agent, DIFFICULTY
from agents import attacking, defensive
from agents.reference import RefAgent

MAX_PLIES = 300

def play_game(white, black, max_plies=MAX_PLIES):
    board = chess.Board()
    moves = []
    while not board.is_game_over(claim_draw=True):
        if len(moves) >= max_plies:
            return "1/2 - 1/2", moves, "Move limit reached"
        agent = white if board.turn == chess.WHITE else black
        move = agent.get_move(board)
        moves.append(board.san(move))

        board.push(move)
    outcome = board.outcome(claim_draw=True)
    return board.result(claim_draw=True), moves, outcome.termination.name.replace("_", " ").title()

def format_moves(moves):
    parts = []
    for i in range(0, len(moves), 2):
        pair = " ".join(moves[i:i+2])
        parts.append(f"{i // 2+1}. {pair}")
    return " ".join(parts)

def run_match(agent1, agent2, games = 8, log_dir="match_logs"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    log_dir = os.path.join(log_dir, f"match_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)

    tally = {agent1.name: 0, agent2.name: 0, "Draws": 0}
    summary = []

    for i in range(games):
        white, black = (agent1, agent2) if i%2 == 0 else (agent2, agent1)
        result, moves, reason = play_game(white, black)

        if result == "1-0":
            tally[white.name] += 1
        elif result == "0-1":
            tally[black.name] += 1
        else:
            tally["Draws"] += 1

        output = (f"Game {i+1}: White={white.name} Black={black.name} "
                f"Result={result} ({reason}, {len(moves)} plies)")

        print(output)
        summary.append(output)
        with open(os.path.join(log_dir, f"game_{i+1}.txt"), "w") as f:
            f.write(output + "\n\n" + format_moves(moves) + "\n")

    score = (f"Final: {agent1.name} {tally[agent1.name]} - "
             f"{tally[agent2.name]} {agent2.name}  (draws: {tally['Draws']})")
    print(score)
    with open(os.path.join(log_dir, "summary.txt"), "w") as f:
        f.write("\n".join(summary) + "\n" + score + "\n")
    return tally

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=8)
    parser.add_argument("--level", default="Medium",  choices = list(DIFFICULTY))
    parser.add_argument("--opponent", default="defensive", choices=["defensive", "random"])
    args = parser.parse_args()

    attk = Agent("Attacking", attacking.evaluate, args.level)
    if args.opponent == "random":
        opp = RefAgent()
    else:
        opp = Agent("Defensive", defensive.evaluate, args.level)
    run_match(attk, opp, games=args.games)