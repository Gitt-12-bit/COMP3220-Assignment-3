import chess
import random

Cmate_Score = 100000
INF=float("inf")
nodes_searched = 0

def terminal_score(board, depth):

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -(Cmate_Score + depth)
        return Cmate_Score + depth

    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    return None

def m_order(board):
    moves = list(board.legal_moves)
    random.shuffle(moves)

    def priority(move):
        val = 0
        if board.is_capture(move):
            victim = board.piece_type_at(move.to_square) or chess.PAWN
            attacker = board.piece_type_at(move.from_square)
            val += 10 + 10 * victim - attacker

        if move.promotion:
            val += 9
        if board.gives_check(move):
            val += 5
        return val

    moves.sort(key=priority, reverse=True)
    return moves

def minimax(board, depth, evaluate):
    global  nodes_searched
    nodes_searched += 1

    over = terminal_score(board, depth)
    if over != None:
        return over
    if depth == 0:
        return evaluate(board)

    moves = list(board.legal_moves)
    if board.turn == chess.WHITE:
        best_move = -INF
        for move in moves:
            board.push(move)
            best_move = max(best_move, minimax(board, depth -1, evaluate))
            board.pop()
        return best_move
    else:
        best_move = INF
        for move in moves:
            board.push(move)
            best_move = min(best_move, minimax(board, depth -1, evaluate))
            board.pop()
        return best_move
        

def alphabeta_search(board, depth, alpha, beta, evaluate):
    global nodes_searched
    nodes_searched += 1

    over = terminal_score(board, depth)

    if over != None:
        return over

    if depth == 0:
        return evaluate(board)

    if board.turn == chess.WHITE:
        best_move = -INF
        for move in m_order(board):
            board.push(move)
            best_move = max(best_move, alphabeta_search(board, depth-1, alpha, beta, evaluate))
            board.pop()
            alpha = max (alpha, best_move)
            if beta <= alpha:
                break
        return best_move
    else:
        best_move = INF
        for move in m_order(board):
            board.push(move)
            best_move = min(best_move, alphabeta_search(board, depth-1, alpha, beta, evaluate))
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                break
        return best_move

def choose_move(board, depth, evaluate):
    moves = m_order(board)
    if not moves:
        return None

    maximize = board.turn == chess.WHITE
    best_move = moves[0]
    best_score = -INF if maximize else INF
    alpha, beta = -INF, INF

    for move in moves:
        board.push(move)
        score = alphabeta_search(board, depth-1, alpha, beta, evaluate)
        board.pop()

        if maximize:
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, best_score)

        else:
            if score < best_score:
                best_score, best_move = score, move
            beta = min(beta,best_score)

    return best_move