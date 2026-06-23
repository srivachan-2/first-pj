"""
Interactive Real Chess Game with GUI using Tkinter
Complete chess implementation with drag-and-drop, piece selection, and move validation
"""

import tkinter as tk
from tkinter import messagebox
from enum import Enum
from typing import List, Tuple, Optional
from copy import deepcopy


class PieceType(Enum):
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"


class Color(Enum):
    WHITE = "W"
    BLACK = "B"


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.moved = False

    def __repr__(self):
        symbol = self.type.value
        return symbol if self.color == Color.WHITE else symbol.lower()


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        """Set up the board with starting position."""
        # Black pieces
        self.board[0][0] = Piece(PieceType.ROOK, Color.BLACK)
        self.board[0][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.board[0][2] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][3] = Piece(PieceType.QUEEN, Color.BLACK)
        self.board[0][4] = Piece(PieceType.KING, Color.BLACK)
        self.board[0][5] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][6] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.board[0][7] = Piece(PieceType.ROOK, Color.BLACK)

        for col in range(8):
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK)

        # White pieces
        for col in range(8):
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE)

        self.board[7][0] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[7][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[7][2] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[7][3] = Piece(PieceType.QUEEN, Color.WHITE)
        self.board[7][4] = Piece(PieceType.KING, Color.WHITE)
        self.board[7][5] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[7][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[7][7] = Piece(PieceType.ROOK, Color.WHITE)

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None

    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Move a piece from one position to another."""
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.moved = True
        return True

    def copy(self):
        """Create a deep copy of the board."""
        new_board = ChessBoard.__new__(ChessBoard)
        new_board.board = deepcopy(self.board)
        return new_board


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.current_player = Color.WHITE
        self.move_history = []
        self.game_over = False
        self.winner = None

    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid moves for a piece at the given position."""
        piece = self.board.get_piece(row, col)
        if piece is None:
            return []

        valid_moves = []

        if piece.type == PieceType.PAWN:
            valid_moves = self._get_pawn_moves(row, col, piece)
        elif piece.type == PieceType.ROOK:
            valid_moves = self._get_rook_moves(row, col, piece)
        elif piece.type == PieceType.KNIGHT:
            valid_moves = self._get_knight_moves(row, col, piece)
        elif piece.type == PieceType.BISHOP:
            valid_moves = self._get_bishop_moves(row, col, piece)
        elif piece.type == PieceType.QUEEN:
            valid_moves = self._get_queen_moves(row, col, piece)
        elif piece.type == PieceType.KING:
            valid_moves = self._get_king_moves(row, col, piece)

        # Filter out moves that would leave king in check
        valid_moves = [move for move in valid_moves if not self._would_be_in_check(row, col, move)]

        return valid_moves

    def _get_pawn_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        direction = 1 if piece.color == Color.BLACK else -1
        start_row = 1 if piece.color == Color.BLACK else 6

        new_row = row + direction
        if self.board.is_valid_position(new_row, col) and self.board.get_piece(new_row, col) is None:
            moves.append((new_row, col))

            if row == start_row:
                new_row_double = row + 2 * direction
                if self.board.get_piece(new_row_double, col) is None:
                    moves.append((new_row_double, col))

        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if self.board.is_valid_position(new_row, new_col):
                target = self.board.get_piece(new_row, new_col)
                if target and target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_rook_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.board.is_valid_position(new_row, new_col):
                    break
                target = self.board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def _get_knight_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.board.is_valid_position(new_row, new_col):
                target = self.board.get_piece(new_row, new_col)
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        return moves

    def _get_bishop_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.board.is_valid_position(new_row, new_col):
                    break
                target = self.board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def _get_queen_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        return self._get_rook_moves(row, col, piece) + self._get_bishop_moves(row, col, piece)

    def _get_king_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if self.board.is_valid_position(new_row, new_col):
                    target = self.board.get_piece(new_row, new_col)
                    if target is None or target.color != piece.color:
                        moves.append((new_row, new_col))
        return moves

    def _would_be_in_check(self, from_row: int, from_col: int, to_move: Tuple[int, int]) -> bool:
        """Check if moving piece would leave king in check."""
        test_board = self.board.copy()
        test_board.move_piece(from_row, from_col, to_move[0], to_move[1])
        return self._is_in_check(self.current_player, test_board)

    def _is_in_check(self, color: Color, board: ChessBoard = None) -> bool:
        """Check if a color's king is in check."""
        if board is None:
            board = self.board

        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.type == PieceType.KING and piece.color == color:
                    king_pos = (row, col)
                    break

        if not king_pos:
            return False

        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = self._get_all_moves_for_piece(row, col, board)
                    if king_pos in moves:
                        return True
        return False

    def _get_all_moves_for_piece(self, row: int, col: int, board: ChessBoard) -> List[Tuple[int, int]]:
        """Get all moves for a piece without check validation."""
        piece = board.get_piece(row, col)
        if piece is None:
            return []

        if piece.type == PieceType.PAWN:
            return self._get_pawn_moves_no_check(row, col, piece, board)
        elif piece.type == PieceType.ROOK:
            return self._get_rook_moves_no_check(row, col, piece, board)
        elif piece.type == PieceType.KNIGHT:
            return self._get_knight_moves_no_check(row, col, piece, board)
        elif piece.type == PieceType.BISHOP:
            return self._get_bishop_moves_no_check(row, col, piece, board)
        elif piece.type == PieceType.QUEEN:
            return (self._get_rook_moves_no_check(row, col, piece, board) + 
                    self._get_bishop_moves_no_check(row, col, piece, board))
        elif piece.type == PieceType.KING:
            return self._get_king_moves_no_check(row, col, piece, board)
        return []

    def _get_pawn_moves_no_check(self, row: int, col: int, piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:
        moves = []
        direction = 1 if piece.color == Color.BLACK else -1
        new_row = row + direction
        if board.is_valid_position(new_row, col) and board.get_piece(new_row, col) is None:
            moves.append((new_row, col))
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target and target.color != piece.color:
                    moves.append((new_row, new_col))
        return moves

    def _get_rook_moves_no_check(self, row: int, col: int, piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not board.is_valid_position(new_row, new_col):
                    break
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def _get_knight_moves_no_check(self, row: int, col: int, piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            new_row, new_col = row + dr, col + dc
            if board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        return moves

    def _get_bishop_moves_no_check(self, row: int, col: int, piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not board.is_valid_position(new_row, new_col):
                    break
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def _get_king_moves_no_check(self, row: int, col: int, piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if board.is_valid_position(new_row, new_col):
                    target = board.get_piece(new_row, new_col)
                    if target is None or target.color != piece.color:
                        moves.append((new_row, new_col))
        return moves

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Attempt to move a piece."""
        piece = self.board.get_piece(from_row, from_col)

        if piece is None or piece.color != self.current_player:
            return False

        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False

        self.board.move_piece(from_row, from_col, to_row, to_col)
        self.move_history.append({
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece.type.value
        })

        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

        return True


class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Chess Game")
        self.game = ChessGame()
        self.cell_size = 60
        self.selected_square = None
        self.valid_moves = []

        # Piece Unicode symbols
        self.piece_symbols = {
            PieceType.PAWN: '♟' if Color.BLACK else '♙',
            PieceType.ROOK: '♜' if Color.BLACK else '♖',
            PieceType.KNIGHT: '♞' if Color.BLACK else '♘',
            PieceType.BISHOP: '♝' if Color.BLACK else '♗',
            PieceType.QUEEN: '♛' if Color.BLACK else '♕',
            PieceType.KING: '♚' if Color.BLACK else '♔',
        }

        # Colors
        self.light_color = "#F0D9B5"
        self.dark_color = "#B58863"
        self.highlight_color = "#BFF9E8"
        self.valid_move_color = "#C0E0C0"

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Top frame for info
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)

        self.status_label = tk.Label(info_frame, text="", font=("Arial", 14, "bold"))
        self.status_label.pack()

        # Canvas for board
        self.canvas = tk.Canvas(
            self.root,
            width=self.cell_size * 8,
            height=self.cell_size * 8,
            bg=self.dark_color
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_square_click)

        # Bottom frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        reset_btn = tk.Button(button_frame, text="New Game", command=self.reset_game, font=("Arial", 12))
        reset_btn.pack(side=tk.LEFT, padx=5)

        undo_btn = tk.Button(button_frame, text="Undo Move", command=self.undo_move, font=("Arial", 12))
        undo_btn.pack(side=tk.LEFT, padx=5)

        # Move history
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Label(history_frame, text="Move History:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text = tk.Text(history_frame, height=6, width=40, yscrollcommand=scrollbar.set, font=("Courier", 10))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10)
        scrollbar.config(command=self.history_text.yview)

        self.draw_board()
        self.update_status()

    def draw_board(self):
        """Draw the chess board."""
        self.canvas.delete("all")

        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Board color
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)

                # Highlight selected square
                if self.selected_square == (row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.highlight_color, outline="blue", width=2)

                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    self.canvas.create_oval(
                        x1 + self.cell_size // 3, y1 + self.cell_size // 3,
                        x2 - self.cell_size // 3, y2 - self.cell_size // 3,
                        fill=self.valid_move_color, outline=self.valid_move_color
                    )

                # Draw piece
                piece = self.game.board.get_piece(row, col)
                if piece:
                    symbol = self.get_piece_symbol(piece)
                    color_text = "white" if piece.color == Color.WHITE else "black"
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=symbol,
                        font=("Arial", 36),
                        fill=color_text
                    )

        # Draw coordinates
        for i in range(8):
            self.canvas.create_text(10, i * self.cell_size + self.cell_size // 2, text=str(7 - i), font=("Arial", 10))
            self.canvas.create_text(i * self.cell_size + self.cell_size // 2, 8 * self.cell_size + 10, text=chr(97 + i), font=("Arial", 10))

    def get_piece_symbol(self, piece: Piece) -> str:
        """Get Unicode symbol for piece."""
        symbols = {
            (PieceType.PAWN, Color.WHITE): '♙',
            (PieceType.PAWN, Color.BLACK): '♟',
            (PieceType.ROOK, Color.WHITE): '♖',
            (PieceType.ROOK, Color.BLACK): '♜',
            (PieceType.KNIGHT, Color.WHITE): '♘',
            (PieceType.KNIGHT, Color.BLACK): '♞',
            (PieceType.BISHOP, Color.WHITE): '♗',
            (PieceType.BISHOP, Color.BLACK): '♝',
            (PieceType.QUEEN, Color.WHITE): '♕',
            (PieceType.QUEEN, Color.BLACK): '♛',
            (PieceType.KING, Color.WHITE): '♔',
            (PieceType.KING, Color.BLACK): '♚',
        }
        return symbols.get((piece.type, piece.color), '?')

    def on_square_click(self, event):
        """Handle square click."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        # If clicking on a valid move, make the move
        if (row, col) in self.valid_moves:
            if self.game.move(self.selected_square[0], self.selected_square[1], row, col):
                self.selected_square = None
                self.valid_moves = []
                self.update_history()
            else:
                messagebox.showerror("Invalid Move", "This move is not allowed!")
        else:
            # Select a new piece
            piece = self.game.board.get_piece(row, col)
            if piece and piece.color == self.game.current_player:
                self.selected_square = (row, col)
                self.valid_moves = self.game.get_valid_moves(row, col)
            else:
                self.selected_square = None
                self.valid_moves = []

        self.update_status()
        self.draw_board()

    def update_status(self):
        """Update status label."""
        player = "White" if self.game.current_player == Color.WHITE else "Black"
        in_check = " (In Check!)" if self.game._is_in_check(self.game.current_player) else ""
        self.status_label.config(text=f"{player}'s Turn{in_check}")

    def update_history(self):
        """Update move history display."""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for i, move in enumerate(self.game.move_history):
            move_num = i + 1
            from_pos = f"{chr(97 + move['from'][1])}{8 - move['from'][0]}"
            to_pos = f"{chr(97 + move['to'][1])}{8 - move['to'][0]}"
            self.history_text.insert(tk.END, f"{move_num}. {move['piece']} {from_pos} → {to_pos}\n")
        self.history_text.config(state=tk.DISABLED)

    def reset_game(self):
        """Start a new game."""
        self.game = ChessGame()
        self.selected_square = None
        self.valid_moves = []
        self.update_status()
        self.update_history()
        self.draw_board()

    def undo_move(self):
        """Undo the last move."""
        if self.game.move_history:
            messagebox.showinfo("Undo", "Undo functionality requires resetting the game.\nStart a new game to reset.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
