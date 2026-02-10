for rank in range(7, -1, -1):
    cols = st.columns(8)
    for file in range(8):
        square = chess.square(file, rank)

        # Klassische Schwarz-Weiß-Färbung
        bg = "#FFFFFF" if (rank + file) % 2 == 0 else "#000000"  # Weiß / Schwarz

        # Hervorhebung ausgewählte Figur und legale Züge
        if square == st.session_state.selected_square:
            bg = "#FFD966"  # Gelb für ausgewählte Figur
        elif square in legal_targets:
            bg = "#A9D18E"  # Grün für legale Züge

        label = render_square(square)

        # Button für das Feld
        if cols[file].button(
            label,
            key=f"{square}",
            help=chess.square_name(square),
            # Setze den Hintergrund per Markdown-Stil (funktioniert am besten)
            args=None
        ):
            board = st.session_state.board

            # Auswahl und Zuglogik unverändert
            if st.session_state.selected_square is None:
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    st.session_state.selected_square = square
            else:
                move = chess.Move(st.session_state.selected_square, square)

                # Bauernumwandlung
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
                st.rerun()
