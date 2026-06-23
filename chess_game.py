"""
A complete chess game implementation with piece movement, turn management, and game state.
"""

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
        self.moved = False  # Track if piece has moved (for castling/pawn double move)

    def __repr__(self):
        symbol = self.type.value
        return symbol if self.color == Color.WHITE else symbol.lower()


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        """Set up the board with starting position."""
        # Black pieces (top of board)
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

        # White pieces (bottom of board)
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

    def display(self):
        """Print the current board state."""
        print("\n    0   1   2   3   4   5   6   7")
        print("  +---+---+---+---+---+---+---+---+")
        for row in range(8):
            print(f"{row} | ", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(f"{piece} | ", end="")
                else:
                    print("  | ", end="")
            print()
            print("  +---+---+---+---+---+---+---+---+")

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

        return valid_moves

    def _get_pawn_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        direction = 1 if piece.color == Color.BLACK else -1
        start_row = 1 if piece.color == Color.BLACK else 6

        # Move forward
        new_row = row + direction
        if self.board.is_valid_position(new_row, col) and self.board.get_piece(new_row, col) is None:
            moves.append((new_row, col))

            # Double move from start
            if row == start_row:
                new_row_double = row + 2 * direction
                if self.board.get_piece(new_row_double, col) is None:
                    moves.append((new_row_double, col))

        # Capture diagonally
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
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
        # Queen moves like both rook and bishop
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

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Attempt to move a piece. Returns True if successful."""
        piece = self.board.get_piece(from_row, from_col)

        if piece is None or piece.color != self.current_player:
            return False

        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False

        # Make the move
        self.board.move_piece(from_row, from_col, to_row, to_col)
        self.move_history.append({
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece.type.value
        })

        # Switch player
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

        return True

    def play(self):
        """Main game loop for interactive play."""
        print("Welcome to Chess!")
        print("Enter moves as: from_row from_col to_row to_col")
        print("Example: 6 4 4 4 (moves piece from row 6, col 4 to row 4, col 4)")
        print("Type 'quit' to exit\n")

        while not self.game_over:
            self.board.display()
            player_color = "White" if self.current_player == Color.WHITE else "Black"
            print(f"\n{player_color}'s turn")

            try:
                user_input = input("Enter move: ").strip()

                if user_input.lower() == 'quit':
                    print("Game ended.")
                    break

                parts = user_input.split()
                if len(parts) != 4:
                    print("Invalid input. Please enter 4 numbers.")
                    continue

                from_row, from_col, to_row, to_col = map(int, parts)

                if self.move(from_row, from_col, to_row, to_col):
                    print(f"Moved from ({from_row}, {from_col}) to ({to_row}, {to_col})")
                else:
                    print("Invalid move. Try again.")

            except ValueError:
                print("Invalid input. Please enter numbers only.")
            except IndexError:
                print("Move out of bounds.")

    def get_game_status(self) -> str:
        """Return current game status."""
        player = "White" if self.current_player == Color.WHITE else "Black"
        return f"Current player: {player}\nMoves played: {len(self.move_history)}"


if __name__ == "__main__":
    game = ChessGame()
    game.play()
