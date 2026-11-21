import tkinter as tk
import threading #Lets AI think in the background to prevent the window freezing
import traceback #Prints error if the AI crashes instead of hanging silently
import chess
from agents.base_agent import Agent, DIFFICULTY #Also imports the difficulty to use in the menus
from agents import attacking, defensive 

SQUARE = 70   # size of one square in pixels

root = tk.Tk()
root.title("ChessBoard")
LEVELS = list(DIFFICULTY.keys())    #Gets difficulties (East, Medium, Hard, Expert)
level_var = tk.StringVar(value="Medium")    #Difficulty for human vs AI
attacking_level_var = tk.StringVar(value="Medium")  #Default difficulty of attacking agent in AI vs AI
defending_level_var = tk.StringVar(value="Medium")  #Default difficulty of defending agent in AI vs AI
attacking_colour_var = tk.StringVar(value="Black")  #Colour attacking agent plays in AI vs AI
white_agent = Agent("Defensive", defensive.evaluate, 2)   # CHANGED: depth=2 -> 2 (matches new Agent)
black_agent = Agent("Attack", attacking.evaluate, 2)      #Attacking agent
canvas = tk.Canvas(root, width=8 * SQUARE, height=8 * SQUARE)
canvas.pack()

#label under the board that shows whose turn it is / the result
status = tk.Label(root, text="", font=("Arial", 14))
status.pack()

#Draws out the structure the board for the game
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
last_move = None   #Last move played (Allows for the two squares to be highlighted)
thinking = False   #True while AI is searching in bakcground
paused = False     #AI vs AI pause switch
step_requested = False  #Set the step button while paused

#Pixel rectangle of a square
def square_box(square):
    col = chess.square_file(square)
    row = 7 - chess.square_rank(square)
    return col * SQUARE, row * SQUARE, (col + 1) * SQUARE, (row + 1) * SQUARE

#Colours last move, selected piece, and king in check
def draw_highlights():
    colours = {}
    if last_move is not None:
        colours[last_move.from_square] = "#cdd26a"
        colours[last_move.from_square] = "#cdd26a"
    if board.is_check():
        colours[board.king(board.turn)] = "#e57373"
    if selected is not None:
        colours[selected] = "#6fa8dc"
    for square, colour in colours.items():
        x1, y1, x2, y2 = square_box(square)
        canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="", tags="highlight")

#Produces dots on empty squares which show the spaces where the selected piece can go, as well as rings on the squares where a piece can be captured
def move_hints():
    if selected is None:
        return
    for move in board.legal_moves:
        if move.from_square != selected:
            continue
        x1, y1, x2, y2 = square_box(move.to_square)
        cx,  cy = (x1 + x2) // 2, (y1 + y2) // 2
        if board.piece_at(move.to_square):
            canvas.create_oval(cx - 30, cy - 30, cx + 30, cy - 30, outline="#444444", width=4, tags="highlight")
        else:
            canvas.create_oval(cx - 9, cy - 9, cx + 9, cy - 9, fill="#555555", outline="", width=4, tags="highlight")

#Draws out the chess pieces
def draw_pieces():
    canvas.delete("piece")          # erase old pieces before redrawing
    canvas.delete("highlight")      #erase old hihglights and hints too
    draw_highlights()               #drawn BEFORE the pieces so they sit underneath
    for square, piece in board.piece_map().items():
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)

        x = col * SQUARE + SQUARE // 2
        y = row * SQUARE + SQUARE // 2
        symbol = SYMBOLS[(piece.piece_type, piece.color)]
        canvas.create_text(x, y, text=symbol, font=("Arial", 40), tags="piece")
    move_hints()    #drawn AFTER the pieces so the capture rings are visible

#shows whose turn it is, or the result when the game ends
def update_status():
    if board.is_game_over(claim_draw=True):
        status.config(text="Game over: " + board.result(claim_draw=True))
    elif thinking:
        status.config(text="Thinking...")   #Tells player the AI is working
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

#Runs the AI in a background thread, then calls the on_done(move) back on the main thread. tkinter is not thread-safe, 
# so the thread NEVER touches a widget: it only stores its answer, and a timer (root.after) picks the answer up.
def think(agent, gid, on_done):
    global thinking
    thinking = True
    update_status()
    snapshot = board.copy()     #the thread searches a copy and not the actual board
    result = {}

    def work():
        try:
            result["move"] = agent.choose_move(snapshot)
        except Exception:
            traceback.print_exc()   #shows the bug in the terminal instead of freezing silently
            result["move"] = None

    def poll():
        global thinking
        if "move" not in result:
            root.after(50, poll)
            return
        if gid == game_id:
            thinking = False
            on_done(result["move"])

    threading.Thread(target=work, daemon=True).start()
    root.after(50, poll)

def agent_reply(gid):   #gid so an old game's reply is ignored
    """Ask the agent for a move, play it, and redraw."""
    if gid != game_id or board.is_game_over(claim_draw=True):
        return
    think(black_agent, gid, finish_reply)   #black_agent is the opponent

#Second half of the agent_reply; causes the game to play the move the AI chose
def finish_reply(move):
    global last_move
    if move is not None:
        board.push(move)
        last_move = move
        draw_pieces()
        update_status()

def on_click(event):
    """First click selects a piece, second click tries to move it."""
    global selected
    if mode != "human":      #clicks only work in human mode
        return

    #Ignore clicks while the AI is thinking, when it's not White's turn, or after the game ends
    if thinking or board.turn != chess.WHITE or board.is_game_over(claim_draw=True):
        return
    square = click_to_square(event)

    if selected is None:
        piece = board.piece_at(square)
        if piece is not None and piece.color == board.turn:
            selected = square
            draw_pieces()
    else:
        other = board.piece_at(square)
        if other is not None and other.color == board.turn:
            selected = square
            draw_pieces()
            return
        move = chess.Move(selected, square)
        #auto-promote a pawn to a queen when it reaches the last row
        piece = board.piece_at(selected)
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) == 7:
            move = chess.Move(selected, square, promotion=chess.QUEEN)
        if move in board.legal_moves:
            board.push(move)
            last_move = move    #remember the last move for the highlight
            selected = None
            draw_pieces()
            update_status()
            if not board.is_game_over(claim_draw=True):
                root.after(100, lambda gid=game_id: agent_reply(gid))
        selected = None
        draw_pieces()
        
        
def agent_vs_agent_step(gid):   #gid so an old game's loop stops
    global step_requested
    if gid != game_id:
        return
    if board.is_game_over(claim_draw=True):
        print("Game over:", board.result(claim_draw=True))
        update_status()
        return
    #While paused, check every 100ms until Step or Resume is pressed
    if paused and not step_requested:
        root.after(100, lambda: agent_vs_agent_step(gid))
        return
    step_requested = False
    current = white_agent if board.turn == chess.WHITE else black_agent

    #The search runs in the background. play_move is the second half of agent_vs_agent_step
    def play_move(move):
        global last_move
        if move is None:
            return
        board.push(move)
        last_move = move
        draw_pieces()
        update_status()
        root.after(500, lambda: agent_vs_agent_step(gid)) 

    think(current, gid, play_move)

# ---------- Control Buttons -----------
def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")

def step_once():
    global step_requested
    if paused:
        step_requested = True

def undo_move():
    global selected, last_move, game_id
    if mode != "human" or thinking or not board.move_stack:
        return
    game_id += 1    #Cancels an AI reply that is still waiting to start
    board.pop()     #AI's reply or your move if AI had not answered yet
    if board.turn != chess.WHITE and board.move_stack:
        board.pop()
    selected = None
    last_move = board.peek() if board.move_stack else None
    draw_pieces()
    update_status()

# ---------------- menu ----------------
menu_frame = tk.Frame(root)

#Clears Menu
def clear_menu():
    for w in menu_frame.winfo_children():
        w.destroy()

#Starts game
def start_game(new_mode, opponent=None, white=None):
    """Reset the board and start either human vs AI or AI vs AI."""
    global board, selected, mode, game_id, black_agent, white_agent
    global last_move, thinking, paused, step_requested
    board = chess.Board()
    selected = None
    last_move = None
    thinking = False
    paused = False
    step_requested = False
    mode = new_mode
    game_id += 1                      # cancels any old agent loop

    if opponent is not None:
        black_agent = opponent        # in human mode the human is White

    if white is not None:
        white_agent = white             #in AI vs AI bth agents are chosen in menu

    menu_frame.pack_forget()
    canvas.pack()
    status.pack()

    #Show buttons that fit the mode
    for button in (undo_button, pause_button, step_button):
        button.pack_forget()
    if mode == "human":
        undo_button.pack(side="left", padx=4)
    else:
        pause_button.config(text="Pause")
        pause_button.pack(side="left", padx=4)
        step_button.pack(side="left", padx=4)

    control_frame.pack()
    back_button.pack()
    canvas.delete("all")
    draw_board()
    draw_pieces()
    update_status()
    if mode == "aiai":
        root.after(500, lambda gid=game_id: agent_vs_agent_step(gid))

#Displays menu
def show_menu():
    global game_id
    game_id += 1                      # stop any running agent loop
    thinking = False
    canvas.pack_forget()
    status.pack_forget()
    control_frame.pack_forget()
    back_button.pack_forget()
    main_menu()

#Shows main menu
def main_menu():
    clear_menu()
    menu_frame.pack(padx=40, pady=40)
    tk.Label(menu_frame, text="Chess Agents", font=("Arial", 22)).pack(pady=10)
    tk.Button(menu_frame, text="Human vs AI", width=20, font=("Arial", 14),
              command=opponent_menu).pack(pady=6)
    tk.Button(menu_frame, text="AI vs AI", width=20, font=("Arial", 14),
              command=aiai_menu).pack(pady=6)


def opponent_menu():
    clear_menu()
    tk.Label(menu_frame, text="Play against:", font=("Arial", 18)).pack(pady=10)
    tk.Label(menu_frame, text="Difficulty:", font=("Arial", 12)).pack()
    tk.OptionMenu(menu_frame, level_var, *LEVELS).pack(pady=6)
    
    tk.Button(menu_frame, text="Defensive agent", width=20, font=("Arial", 14),
                  command=lambda: start_game("human", Agent("Defensive", defensive.evaluate, level_var.get()))).pack(pady=6)
        
    tk.Button(menu_frame, text="Attacking agent", width=20, font=("Arial", 14),
                      command=lambda: start_game("human", Agent("Attack", attacking.evaluate, level_var.get()))).pack(pady=6)
    
    tk.Button(menu_frame, text="Back", command=main_menu).pack(pady=6)
    
def aiai_menu():
    clear_menu()
    tk.Label(menu_frame, text="AI vs AI", font=("Arial", 18)).pack(pady=10)
    tk.Label(menu_frame, text="Attacking agent difficulty:", font=("Arial", 12)).pack()

    tk.OptionMenu(menu_frame, attacking_level_var, *LEVELS).pack(pady=4)
    tk.Label(menu_frame, text="Defensive agent difficulty:", font=("Arial", 12)).pack()
    tk.OptionMenu(menu_frame, defending_level_var, *LEVELS).pack(pady=4)

    tk.Label(menu_frame, text="Attacking agent plays:", font=("Arial", 12)).pack()
    tk.OptionMenu(menu_frame, attacking_colour_var, "White", "Black").pack(pady=4)

    tk.Button(menu_frame, text="Start", width=20, font=("Arial", 14),
              command=start_aiai).pack(pady=8)
    
    tk.Button(menu_frame, text="Back", command=main_menu).pack(pady=6)

def start_aiai():
    attack = Agent("Attack", attacking.evaluate, attacking_level_var.get())
    defend = Agent("Defensive", defensive.evaluate, defending_level_var.get())
    if attacking_colour_var.get() == "White":
        start_game("aiai", opponent=defend, white=attack)
    else:
        start_game("aiai", opponent=attack, white=defend)

back_button = tk.Button(root, text="Menu", command=show_menu)

#frame holding mode-specific buttons (Undo, Pause, Step)
control_frame = tk.Frame(root)
undo_button = tk.Button(control_frame, text="Undo", command=undo_move)
pause_button = tk.Button(control_frame, text="Pause", command=toggle_pause)
step_button = tk.Button(control_frame, text="Step", command=step_once)

canvas.bind("<Button-1>", on_click)

#Start up lines inside run() function, so importing this file doesn't start the program.
#Main.py can call gui.run(agents)
def run(agents=None):
    # start on the menu instead of going straight into a game
    canvas.pack_forget()
    status.pack_forget()
    main_menu()
    root.mainloop()

if __name__ == "__main__":
    run()