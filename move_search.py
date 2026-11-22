#ID NUMBERS: 620171757, 620160983
import chess
import random

Cmate_Score = 100000
INF=float("inf")
nodes_searched = 0

#Sets the node counter back to 0 which allows a new search to be measured on it's own
def reset_node_count():
    global nodes_searched
    nodes_searched = 0

#Returns how many positions (nodes) the search has visited since the last reset.
def get_node_count():
    return nodes_searched

#Return the score of a finished game or None if game is still going
#Checked before the depth cutoff so search never walks past a forced mate
def terminal_score(board, depth):

    #The side to move is the one that got mated. Adding depth makes faster mates score higher.
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -(Cmate_Score + depth)
        return Cmate_Score + depth

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    #A position that already happened once counts as a draw, so a winning agent can't shuffle pieces forever.
    if board.is_repetition(2):
        return 0
    return None

#Return legal moves with captures, promotions and checks first, because alpha-beta prunes more when good moves are tried early.
#The list is shuffled first so equally good moves come out in random order.
def m_order(board):
    moves = list(board.legal_moves)
    random.shuffle(moves)

    #Gives a move a priority score: capturing a valuable piece with a cheap one ranks highest, then promotions, then checks.
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

#Minimax with no pruning, used to compare against alpha-beta. Scores are from white's pov.
#White picks the highest score and Black picks the lowest. best_move holds the best score found so far.
def minimax(board, depth, evaluate):
    global  nodes_searched
    nodes_searched += 1

    over = terminal_score(board, depth)
    if over != None:
        return over
    if depth == 0:
        # If depth limit reached, stop looking ahead and score the position.
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
        
#Minimax with alpha-beta pruning: returns the same score as minimax() but visits far fewer positions.
#Alpha is the best score White is already guaranteed and beta is the best score Black is already guaranteed.
def alphabeta_search(board, depth, alpha, beta, evaluate):
    global nodes_searched
    nodes_searched += 1

    over = terminal_score(board, depth)

    if over != None:
        return over

    if depth == 0:
        # If depth limit reached, stop looking ahead and score the position.
        return evaluate(board)

    if board.turn == chess.WHITE:
        best_move = -INF
        for move in m_order(board):
            board.push(move)
            best_move = max(best_move, alphabeta_search(board, depth-1, alpha, beta, evaluate))
            board.pop()
            alpha = max (alpha, best_move)
            if beta <= alpha:
                #Prune: Black would never allow this line, so the remaining moves can't change the result.
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
                #Prune: White would never allow this line, so the remaining moves can't change the result.
                break
        return best_move

#Top-level search which tries every legal move with alphabeta_search and returns the best MOVE for the side to play.
#Depth sets how many plies ahead the agent looks. Returns None if there are no legal moves.
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