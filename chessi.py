import streamlit as st
import chess

st.set_page_config(page_title="Streamlit Chess", layout="centered")

# ---------- Session State ----------
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "selected_square" not in st.session_state:
    st.session_state.selected_square = None
if "move_stack" not in st.session_state:
    st.session_state.move_stack = []

# ---------- Helpers ----------
UNICODE_PIECES = {
    "P": "♙", "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔",
    "p": "♟", "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚",
}

def render_square(square):
    piece = st.session_state.board.piece_at(square)
    return UNICODE_PIECES[piece.symbol()] if piece else " "

def legal_moves_from(square):
    return [m.to_square for m in st.session_state.board.legal_moves if m.from_square == square]

def reset_game():
    st.session_state.board = chess.Board()
    st.session_state.selected_square = None
    st.session_state.move_stack = []

def undo_move():
    if st.session_state.move_stack:
        st.session_state.board.pop()
        st.session_state.move_stack.pop()
        st.session_state.selected_square = None

# ---------- Header ----------
st.title("♟️ Streamlit Schach – 2 Spieler")
st.caption("Lokales Zwei-Spieler-Schach mit vollständigen Regeln")

# ---------- Status ----------
turn = "Weiß" if st.session_state.board.turn else "Schwarz"
status = f"**{turn} am Zug**"

if st.session_state.board.is_checkmate():
    status = "♚ **Schachmatt**"
elif st.session_state.board.is_check():
    status += " — **Schach**"
elif st.session_state.board.is_stalemate():
    status = "⚖️ **Patt**"

st.markdown(status)

# ---------- Controls ----------
col1, col2, col3 = st.columns(3)
with col1:
    st.button("🔄 Neues Spiel", on_click=reset_game)
with col2:
    st.button("↩️ Zug rückgängig", on_click=undo_move)
with col3:
    st.button("🧹 Spiel zurücksetzen", on_click=reset_game)

st.divider()

# ---------- Board ----------
legal_targets = []
if st.session_state.selected_square is not None:
    legal_targets = legal_moves_from(st.session_state.selected_square)

for rank in range(7, -1, -1):
    cols = st.columns(8)
    for file in range(8):
        square = chess.square(file, rank)

        bg = "#EEEED2" if (rank + file) % 2 == 0 else "#769656"

        if square == st.session_state.selected_square:
            bg = "#FFD966"
        elif square in legal_targets:
            bg = "#A9D18E"

        label = render_square(square)

        if cols[file].button(
            label,
            key=f"{square}",
            help=chess.square_name(square),
        ):
            board = st.session_state.board

            # Select piece
            if st.session_state.selected_square is None:
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    st.session_state.selected_square = square

            # Make move
            else:
                move = chess.Move(st.session_state.selected_square, square)

                # Promotion handling
                if board.piece_at(st.session_state.selected_square).piece_type == chess.PAWN:
                    if chess.square_rank(square) in [0, 7]:
                        promo = st.selectbox(
                            "Figur für Umwandlung wählen:",
                            ["Dame", "Turm", "Läufer", "Springer"],
                            key="promotion"
                        )
                        promo_map = {
                            "Dame": chess.QUEEN,
                            "Turm": chess.ROOK,
                            "Läufer": chess.BISHOP,
                            "Springer": chess.KNIGHT,
                        }
                        move.promotion = promo_map[promo]

                if move in board.legal_moves:
                    board.push(move)
                    st.session_state.move_stack.append(move)

                st.session_state.selected_square = None
                st.experimental_rerun()

# ---------- Footer ----------
st.divider()
st.caption("✔️ Volle Regeln • ✔️ Legale Züge hervorgehoben • ✔️ Zwei Spieler an einem Gerät")
