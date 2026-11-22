#ID NUMBERS: 620171757, 620160983
import sys
import chess
import move_search as search
from agents import attacking, defensive

POSITIONS = {
    "Starting position": chess.STARTING_FEN,
    "Italian Game opening": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
}

EVALUATORS = {"Attacking": attacking.evaluate, "Defensive": defensive.evaluate}

#Searches one position with one evaluation function with ot without pruning and returns(score, number of nodes visited)
#The node counter is reset before each search so the counts never mix.
def count_nodes(fen, depth, use_pruning, evaluate):
    board = chess.Board(fen)
    search.reset_node_count()

    if use_pruning:
        score = search.alphabeta_search(board, depth, -search.INF, search.INF, evaluate)
    else:
        score = search.minimax(board, depth, evaluate)
    return score, search.get_node_count()

if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for posname, fen in POSITIONS.items():
        for agentname, evaluate in EVALUATORS.items():
            s1, n1 = count_nodes(fen, depth, False, evaluate)
            s2, n2 = count_nodes(fen, depth, True, evaluate)
            print(f"{posname} | {agentname} | depth {depth}")
            print(f" Minimax: {n1:>9,} nodes, score {s1} | Alpha-Beta: {n2:>9,} nodes"
                  f"(score {s2}) | Same score: {s1 == s2} | Nodes saved: {100 * (1 - n2 / n1):.1f}%\n")