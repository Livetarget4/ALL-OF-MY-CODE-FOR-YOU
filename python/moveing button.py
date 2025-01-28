import tkinter as tk
import random

class ClickButtonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Click the Moving Button")
        
        # Create a canvas for drawing the button
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Initialize score and other variables
        self.score = 0
        self.time_limit = 30  # Time limit in seconds
        self.game_over = False

        # Display score on the window
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 12))

        # Add a larger button that moves around
        self.button = tk.Button(self.root, text="Click Me!", command=self.on_button_click, font=("Arial", 16, "bold"))
        self.button_window = self.canvas.create_window(random.randint(50, 350), random.randint(50, 350), window=self.button)

        # Start the game timer
        self.start_time = self.root.after(1000, self.update_timer)
        self.timer_label = self.canvas.create_text(200, 10, text=f"Time: {self.time_limit}", font=("Arial", 12))

        # Start the game loop
        self.move_button()

    def move_button(self):
        if self.game_over:
            return

        # Move the button to a new random position on the canvas
        new_x = random.randint(50, 350)
        new_y = random.randint(50, 350)

        self.canvas.coords(self.button_window, new_x, new_y)

        # Call the move_button method again after a longer delay to make the button move slower
        self.root.after(1000, self.move_button)  # 1000ms = 1 second delay

    def on_button_click(self):
        if self.game_over:
            return

        # Increase score every time the button is clicked
        self.score += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update_timer(self):
        if self.game_over:
            return

        # Decrease time limit and update the timer label
        self.time_limit -= 1
        self.canvas.itemconfig(self.timer_label, text=f"Time: {self.time_limit}")

        if self.time_limit <= 0:
            self.end_game()
        else:
            # Continue updating the timer every second
            self.root.after(1000, self.update_timer)

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(200, 200, text="Game Over!", font=("Arial", 24), fill="red")
        self.canvas.create_text(200, 240, text=f"Final Score: {self.score}", font=("Arial", 16), fill="black")


# Create the Tkinter window and run the game
root = tk.Tk()
game = ClickButtonGame(root)
root.mainloop()
