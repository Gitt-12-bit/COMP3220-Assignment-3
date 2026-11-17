import sys
import chess
import move_search as search
from agents import attacking, defensive

POSITIONS = {
    "Starting position": chess.STARTING_FEN,
}

def count_nodes(fen, depth, use_pruning):
    board = chess.Board(fen)
    search.reset_node_count()

    if use_pruning:
        attkscore = search.alphabeta_search(board, depth, -search.INF, search.INF, attacking.evaluate)
        defscore = search.alphabeta_search(board, depth, -search.INF, search.INF, defensive.evaluate)
    else:
        attkscore = search.minimax(board, depth, attacking.evaluate)
        defscore = search.minimax(board, depth, defensive.evaluate)
    return attkscore, defscore, search.get_node_count()


if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    name, fen = POSITIONS.items()
    s1, n1 = count_nodes(fen, depth, use_pruning=False)
    s2, n2 = count_nodes(fen, depth, use_pruning=True)
    print(f"{name}  (depth {depth})")
    print(f" Minimax: {n1:>9,} nodes, score {s1}")
    print(f" Alpha-Beta: {n2:>9,} nodes, score {s2}")
    print(f" Same score: {s1 == s2} Nodes saved: {100 * (1 - n2 / n1):.1f}%\n")