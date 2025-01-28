import tkinter as tk  
from tkinter import messagebox  

class ChessApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Chess - Black and White")  

        # Chessboard setup  
        self.board = [  
            ["r", "n", "b", "q", "k", "b", "n", "r"],  
            ["p", "p", "p", "p", "p", "p", "p", "p"],  
            [" ", " ", " ", " ", " ", " ", " ", " "],  
            [" ", " ", " ", " ", " ", " ", " ", " "],  
            [" ", " ", " ", " ", " ", " ", " ", " "],  
            [" ", " ", " ", " ", " ", " ", " ", " "],  
            ["P", "P", "P", "P", "P", "P", "P", "P"],  
            ["R", "N", "B", "Q", "K", "B", "N", "R"]  
        ]  

        self.create_chessboard()  
        self.selected_square = None  
        self.current_player = "white"  # White starts first  
        self.update_board()  

    def create_chessboard(self):  
        """Create the chessboard with green and gray alternating colors"""  
        self.squares = {}  
        self.buttons = {}  

        for row in range(8):  
            for col in range(8):  
                square_name = f"{chr(col + 97)}{8 - row}"  
                square_color = '#A0DAB5' if (row + col) % 2 == 0 else '#A9A9A9'  # Green and Gray  

                button = tk.Button(self.root, width=8, height=4, bg=square_color,  
                                   fg="black", font=("Courier", 16, "bold"),  
                                   command=lambda row=row, col=col: self.on_square_click(row, col))  
                button.grid(row=row, column=col)  
                self.squares[square_name] = (row, col)  
                self.buttons[square_name] = button  

    def update_board(self):  
        """Update pieces on the board with player colors"""  
        for square_name, (row, col) in self.squares.items():  
            piece = self.board[row][col]  
            if piece != " ":  
                # Assign colors: black for black pieces, white for white pieces  
                color = "black" if piece.islower() else "white"  
                self.buttons[square_name].config(text=piece, fg=color)  
            else:  
                self.buttons[square_name].config(text="")  

    def end_game(self, winner_color):  
        """End the game and display a message"""  
        messagebox.showinfo("Game Over", f"{winner_color.capitalize()} wins!")  
        self.root.quit()  # Close the application  

    def is_valid_move(self, start_row, start_col, end_row, end_col):  
        """Check if the move is valid for the type of piece"""  
        start_piece = self.board[start_row][start_col]  
        target_piece = self.board[end_row][end_col]  

        # Get the piece type, and find its color  
        piece_color = 'black' if start_piece.islower() else 'white'  
        target_color = 'black' if target_piece.islower() else 'white' if target_piece != " " else None  

        # Prevent moving to a square occupied by own piece  
        if target_color == piece_color:  
            return False  

        # Check movement by piece type  
        difference_row = end_row - start_row  
        difference_col = end_col - start_col  

        if start_piece.lower() == 'p':  # Pawn  
            direction = -1 if start_piece.isupper() else 1  
            # Normal move  
            if start_col == end_col:  
                if difference_row == direction and target_piece == " ":  
                    return True  
                # Double move from initial position  
                if (start_row == 1 and start_piece.islower() or start_row == 6 and start_piece.isupper()) and difference_row == 2 * direction and target_piece == " " and self.board[start_row + direction][start_col] == " ":  
                    return True  
            # Capture  
            if abs(difference_col) == 1 and difference_row == direction and target_piece != " ":  
                return True  

        elif start_piece.lower() == 'r':  # Rook  
            if difference_row == 0 or difference_col == 0:  # Straight move  
                return self.is_path_clear(start_row, start_col, end_row, end_col)  

        elif start_piece.lower() == 'n':  # Knight  
            if (abs(difference_row) == 2 and abs(difference_col) == 1) or (abs(difference_row) == 1 and abs(difference_col) == 2):  
                return True  

        elif start_piece.lower() == 'b':  # Bishop  
            if abs(difference_row) == abs(difference_col):  # Diagonal move  
                return self.is_path_clear(start_row, start_col, end_row, end_col)  

        elif start_piece.lower() == 'q':  # Queen  
            if (difference_row == 0 or difference_col == 0) or (abs(difference_row) == abs(difference_col)):                return self.is_path_clear(start_row, start_col, end_row, end_col)  

        elif start_piece.lower() == 'k':  # King  
            if abs(difference_row) <= 1 and abs(difference_col) <= 1:  
                return True  

        return False  

    def is_path_clear(self, start_row, start_col, end_row, end_col):  
        """Check if the path between two squares is clear for piece movement"""  
        row_step = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0  
        col_step = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0  

        current_row, current_col = start_row + row_step, start_col + col_step  

        while (current_row != end_row or current_col != end_col):  
            if self.board[current_row][current_col] != " ":  
                return False  
            current_row += row_step  
            current_col += col_step  

        return True  

    def on_square_click(self, row, col):  
        """Handle piece movement and switch turns"""  
        square_name = f"{chr(col + 97)}{8 - row}"  
        if self.selected_square:  
            start_row, start_col = self.squares[self.selected_square]  
            piece = self.board[start_row][start_col]  

            # Allow moves only for the current player's pieces and valid moves  
            if (self.current_player == "white" and piece.isupper()) or (self.current_player == "black" and piece.islower()):  
                if self.is_valid_move(start_row, start_col, row, col):  
                    target_piece = self.board[row][col]  

                    # Check if the king is being captured  
                    if target_piece.lower() == 'k':  
                        winner_color = "White" if self.current_player == "white" else "Black"  
                        self.end_game(winner_color)  
                        return  

                    # Move the piece  
                    self.board[row][col] = piece  
                    self.board[start_row][start_col] = " "  
                    self.current_player = "black" if self.current_player == "white" else "white"  # Switch turn  

            self.selected_square = None  
        else:  
            # Select a piece (only for the current player)  
            piece = self.board[row][col]  
            if (self.current_player == "white" and piece.isupper()) or (self.current_player == "black" and piece.islower()):  
                self.selected_square = square_name  

        self.update_board()  

root = tk.Tk()  
app = ChessApp(root)  
root.mainloop()
