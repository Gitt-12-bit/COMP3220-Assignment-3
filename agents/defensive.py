import chess

board = chess.Board()
print(board)


def Material(board):
    # Lookup table containing the value of each chess piece
    
    piece_values ={
        chess.PAWN:1, 
        chess.KNIGHT:3,
        chess.BISHOP:3, 
        chess.ROOK:5, 
        chess.QUEEN:9,
        chess.KING:0
    }
    score= 0
    for piece in board.piece_map().values():
        value =  piece_values[piece.piece_type]
        if piece.color == chess.WHITE:
            score += value
        else:
            score -= value
    return score
    
    
def pawn_shield(board, color):
    # Checks how many friendly pawns are directly in front
    # of the king to help evaluate its protection.
    king_square = board.king(color)    
    file = chess.square_file(king_square)   
    rank = chess.square_rank(king_square)   
    if color == chess.WHITE:
        front_rank = rank + 1
    else:
        front_rank = rank - 1

    count = 0
    for f in [file - 1, file, file + 1]:
        if 0 <= f <= 7 and 0 <= front_rank <= 7:
            square = chess.square(f, front_rank)
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.PAWN and piece.color == color:
                count += 1

    return count

    
    
    board = chess.Board()



def king_tucked(board, color):
    # Checks whether the king is positioned on the c-file
    # or g-file, which may indicate a safer position.
    king_square = board.king(color)
    file = chess.square_file(king_square)

    if file == 2 or file == 6:
        return 1
    return 0


def king_danger(board, color):
    # Measures king danger by counting enemy pieces attacking
    # the squares surrounding the king.
    king_square = board.king(color)
    file = chess.square_file(king_square)
    rank = chess.square_rank(king_square)
    enemy = not color          # the other side

    danger = 0
    for f in [file - 1, file, file + 1]:
        for r in [rank - 1, rank, rank + 1]:
            if 0 <= f <= 7 and 0 <= r <= 7:
                square = chess.square(f, r)
                danger += len(board.attackers(enemy, square))

    return danger
        

def evaluate(board):
    shield_weight = 0.5
    castle_weight = 1.0
    danger_weight = 0.4
    shield = pawn_shield(board, chess.WHITE) - pawn_shield(board, chess.BLACK)
    castle = king_tucked(board, chess.WHITE) - king_tucked(board, chess.BLACK)
    danger = king_danger(board, chess.WHITE) - king_danger(board, chess.BLACK)
    return Material(board) + shield_weight * shield + castle_weight * castle - danger_weight * danger
