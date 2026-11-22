#ID NUMBERS: 620171757, 620160983
'''
The strategy involves Always attacking and never really defending. This specific agent
scores positions by how much pressure it puts on the enemy kind, how active and advanced
its pieces are, and how quickly it develops. It doesn't have a king-safety mechanism so
it will trade it's own safety to complete it's task.

Every function returns a number from WHITE point of view.
'''

import chess

PIECE_VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}

ATTACKING_WEIGHT = {chess.PAWN: 1, chess.KNIGHT: 2, chess.BISHOP: 2,
                    chess.ROOK: 3, chess.QUEEN: 5, chess.KING: 0}

K_pressure_weight = 12
Check_weight = 40
Mobility_weight = 4
Advance_weight = 6
Develop_weight = 15

#Adds up piece values for each side and return white's total minus black's. This is the baseline every position starts from.
def material(board):
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += value * len(board.pieces(piece_type, chess.WHITE))
        score -= value * len(board.pieces(piece_type, chess.BLACK))
    return score

#Measures how hard attacker_color is attacking the squares around the enemy king 
#Stronger attackers such as the queen count more. This is the agent's main aggressive feature.
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

#Gives a bonus to the side that is currently giving check, to reward taking the initiative.
#The side to move is the one in check, so the side giving check is the opposite colou
def check_bonus(board):
    if board.is_check():
        return Check_weight if board.turn == chess.BLACK else -Check_weight
    return 0

#Counts how many squares the knights, bishops, rooks and queens of one colour can reach. More reachable squares means more attacking options.
#It uses attack masks instead of generating legal moves, which is much faster.
def mobility(board, color):
    own_pieces = board.occupied_co[color]
    total = 0
    for piece_type in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        for square in board.pieces(piece_type, color):
            reachable = board.attacks_mask(square) & ~own_pieces
            total += chess.popcount(reachable)
    return total

#Rewards pieces and pawns that have moved up the board toward the enemy side. Black's rank is counted from its own side (7 - rank).
def advancement(board, color):
    total = 0
    for piece_type in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        for square in board.pieces(piece_type, color):
            rank = chess.square_rank(square)
            total += rank if color == chess.WHITE else 7 - rank
    return total

#Counts the knights and bishops that have left their starting back rank, to reward getting pieces into the game quickly.
def development(board, color):
    home_rank = 0 if color == chess.WHITE else 7
    count = 0
    for piece_type in (chess.KNIGHT, chess.BISHOP):
        for square in board.pieces(piece_type, color):
            if chess.square_rank(square) != home_rank:
                count += 1
    return count

#Combines all the features into one score for the position, from White's point of view (positive means White is better).
def evaluate(board):
    score = material(board)
    #White's features are added and Black's are subtracted, so the score always favours White when positive.
    for color, sign in ((chess.WHITE, 1), (chess.BLACK, -1)):
        score  += sign * ( K_pressure_weight * king_pressure(board, color)
                          + Mobility_weight * mobility(board, color)
                          + Advance_weight * advancement(board, color)
                          + Develop_weight * development(board, color)
                          )
    #There is deliberately no king-safety or pawn-structure term, which is what makes this agent attacking.
    score += check_bonus(board)
    return score