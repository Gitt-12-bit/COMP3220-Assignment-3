import tkinter as tk
import chess
from agents.base_agent import Agent
from agents.defensive import evaluate
from agents.defensive import Material #importing my function for testing agent vs agent replace with yours 
SQUARE = 70   # size of one square in pixels

root = tk.Tk()
root.title("ChessBoard")
white_agent = Agent("Defensive", evaluate, 2)   # CHANGED: depth=2 -> 2 (matches new Agent)
black_agent = Agent("Attack", Material, 2)   #your agent here 
canvas = tk.Canvas(root, width=8 * SQUARE, height=8 * SQUARE)
canvas.pack()

#label under the board that shows whose turn it is / the result
status = tk.Label(root, text="", font=("Arial", 14))
status.pack()

def draw_board():
    for row in range(8):
        for col in range(8):
            # alternate colors
            if (row + col) % 2 == 0:
                color = "#f0d9b5"
            else:
                color = "#b58863"
            x1 = col * SQUARE
            y1 = row * SQUARE
            x2 = x1 + SQUARE
            y2 = y1 + SQUARE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            
            
SYMBOLS = {
    (chess.PAWN, chess.WHITE): "♙",   (chess.PAWN, chess.BLACK): "♟",
    (chess.KNIGHT, chess.WHITE): "♘", (chess.KNIGHT, chess.BLACK): "♞",
    (chess.BISHOP, chess.WHITE): "♗", (chess.BISHOP, chess.BLACK): "♝",
    (chess.ROOK, chess.WHITE): "♖",   (chess.ROOK, chess.BLACK): "♜",
    (chess.QUEEN, chess.WHITE): "♕",  (chess.QUEEN, chess.BLACK): "♛",
    (chess.KING, chess.WHITE): "♔",   (chess.KING, chess.BLACK): "♚",
}
board = chess.Board()
selected = None
mode = None        # "human" or "aivai"
game_id = 0        # lets us cancel an old agent loop when a new game starts

def draw_pieces():
    canvas.delete("piece")          # erase old pieces before redrawing
    for square, piece in board.piece_map().items():
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)

        x = col * SQUARE + SQUARE // 2
        y = row * SQUARE + SQUARE // 2
        symbol = SYMBOLS[(piece.piece_type, piece.color)]
        canvas.create_text(x, y, text=symbol, font=("Arial", 40), tags="piece")

#shows whose turn it is, or the result when the game ends
def update_status():
    if board.is_game_over(claim_draw=True):
        status.config(text="Game over: " + board.result(claim_draw=True))
    else:
        if board.turn == chess.WHITE:
            status.config(text="White to move")
        else:
            status.config(text="Black to move")
 
def click_to_square(event):
    col = event.x // SQUARE
    row = event.y // SQUARE
    rank =  7 - row
    return chess.square(col, rank)

def agent_reply(gid):   #gid so an old game's reply is ignored
    """Ask the agent for a move, play it, and redraw."""
    if gid != game_id or board.is_game_over(claim_draw=True):
        return
    move = black_agent.choose_move(board)   #black_agent is the opponent
    if move is not None:
        board.push(move)
        draw_pieces()
        update_status()
        
def on_click(event):
    """First click selects a piece, second click tries to move it."""
    global selected
    if mode != "human":      #clicks only work in human mode
        return
    square = click_to_square(event)

    if selected is None:
        piece = board.piece_at(square)
        if piece is not None and piece.color == board.turn:
            selected = square
    else:
        move = chess.Move(selected, square)
        #auto-promote a pawn to a queen when it reaches the last row
        piece = board.piece_at(selected)
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) == 7:
            move = chess.Move(selected, square, promotion=chess.QUEEN)
        if move in board.legal_moves:
            board.push(move)
            draw_pieces()
            update_status()
            if not board.is_game_over(claim_draw=True):
                root.after(100, lambda: agent_reply(game_id))
        selected = None
        
        
def agent_vs_agent_step(gid):   #gid so an old game's loop stops
    if gid != game_id:
        return
    if board.is_game_over(claim_draw=True):
        print("Game over:", board.result(claim_draw=True))
        update_status()
        return
    current = white_agent if board.turn == chess.WHITE else black_agent
    move = current.choose_move(board)
    board.push(move)
    draw_pieces()
    update_status()
    root.after(500, lambda: agent_vs_agent_step(gid)) 

# ---------------- menu ----------------
menu_frame = tk.Frame(root)

def clear_menu():
    for w in menu_frame.winfo_children():
        w.destroy()

def start_game(new_mode, opponent=None):
    """Reset the board and start either human vs AI or AI vs AI."""
    global board, selected, mode, game_id, black_agent
    board = chess.Board()
    selected = None
    mode = new_mode
    game_id += 1                      # cancels any old agent loop
    if opponent is not None:
        black_agent = opponent        # in human mode the human is White
    menu_frame.pack_forget()
    canvas.pack()
    status.pack()
    back_button.pack()
    canvas.delete("all")
    draw_board()
    draw_pieces()
    update_status()
    if mode == "aiai":
        root.after(500, lambda: agent_vs_agent_step(game_id))

def show_menu():
    global game_id
    game_id += 1                      # stop any running agent loop
    canvas.pack_forget()
    status.pack_forget()
    back_button.pack_forget()
    main_menu()

def main_menu():
    clear_menu()
    menu_frame.pack(padx=40, pady=40)
    tk.Label(menu_frame, text="Chess Agents", font=("Arial", 22)).pack(pady=10)
    tk.Button(menu_frame, text="Human vs AI", width=20, font=("Arial", 14),
              command=opponent_menu).pack(pady=6)
    tk.Button(menu_frame, text="AI vs AI", width=20, font=("Arial", 14),
              command=lambda: start_game("aiai")).pack(pady=6)

def opponent_menu():
    clear_menu()
    tk.Label(menu_frame, text="Play against:", font=("Arial", 18)).pack(pady=10)
    tk.Button(menu_frame, text="Defensive agent", width=20, font=("Arial", 14),
              command=lambda: start_game("human", Agent("Defensive", evaluate, 2))).pack(pady=6)
    tk.Button(menu_frame, text="Attacking agent", width=20, font=("Arial", 14),
              command=lambda: start_game("human", Agent("Attack", Material, 2))).pack(pady=6)   #your agent here
    tk.Button(menu_frame, text="Back", command=main_menu).pack(pady=6)

back_button = tk.Button(root, text="Menu", command=show_menu)

canvas.bind("<Button-1>", on_click)

# start on the menu instead of going straight into a game
canvas.pack_forget()
status.pack_forget()
main_menu()
root.mainloop()