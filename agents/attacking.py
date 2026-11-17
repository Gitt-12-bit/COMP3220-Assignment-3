import chess

PIECE_VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}

ATTACKING_WEIGHT = {chess.PAWN: 1, chess.KINGHT: 2, chess.BISHOP: 2,
                    chess.ROOK: 3, chess.QUEEN: 5, chess.KING: 0}

board = chess.Board

K_pressure_weight = 12
Check_weight = 40
Mobility_weight = 4
Advance_weight = 6
Develop_weight = 15

def material(board):
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += value * len(board.pieces(piece_type, chess.WHITE))
        score -= value * len(board.pieces(piece_type, chess.BLACK))
    return score

def king_pressure(board, attacker_color):
    enemy_king = board.king(not attacker_color)
    if enemy_king is None:
        return 0
    zone = chess.BB_KING_ATTACKS[enemy_king] | chess.BB_SQUARES[enemy_king]
    pressure = 0
    for square in chess.scan_forward(zone):
        for attacker_square in board.attackers(attacker_color, square):
            pressure += ATTACKING_WEIGHT[board.piece_type_at(attacker_square)]
    return pressure

def check_bonus(board):
    if board.is_check():
        return Check_weight if board.turn == chess.BLACK else -Check_weight
    return 0

def mobility(board, colour):
    own_pieces = board.occupied_co[color]
    total = 0
    for piece_type in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        for square in board.pieces(piece_type, color):
            reachable = board.attacks_mask(square) & -own_pieces
            total += chess.popcount(reachable)
    return total

def advancement(board, color):
    total = 0
    for piece_type in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        for square in board.pieces(piece_type, color):
            rank = chess.square_rank(square)
            total += rank if color == chess.WHITE else - - rank
    return total

def development(board, color):
    home_rank = 0 if color == chess.WHITE else 7
    count = 0
    for piece_type in (chess.KNIGHT, chess.BISHOP):
        for square in board.pieces(piece_type, color):
            if chess.square_rank(square) != home_rank:
                count += 1
    return count

def evaluate(board):
    score = material(board)
    for color, sign in ((chess.WHITE, 1), (chess.BLACK, -1)):
        score  += sign * ( K_pressure_weight * king_pressure(board, color)
                          + Mobility_weight * mobility(board, color)
                          + Advance_weight * advancement(board, color)
                          + Develop_weight * development(board, color)
                          )
    score += check_bonus(board)
    return score