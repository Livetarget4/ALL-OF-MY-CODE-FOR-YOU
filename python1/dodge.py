import tkinter as tk
import random
import time  # We will use this to track actual elapsed time.

# Set up the game window
WIDTH = 400
HEIGHT = 600
FPS = 30

class DodgeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dodge the Falling Objects")

        # Create a canvas to draw on
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Initialize the player (a red rectangle)
        self.player_width = 40
        self.player_height = 20
        self.player = self.canvas.create_rectangle(WIDTH // 2 - self.player_width // 2, HEIGHT - self.player_height - 10,
                                                   WIDTH // 2 + self.player_width // 2, HEIGHT - 10, fill="red")

        # Initialize falling objects
        self.objects = []
        
        # Game state
        self.score = 0
        self.is_game_over = False
        self.difficulty = 1  # Difficulty increases over time
        self.start_time = time.time()  # Track actual game time
        
        # Bind key events
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Display Score and Timer
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="Score: 0", fill="white", font=("Arial", 12))
        self.timer_text = self.canvas.create_text(WIDTH - 10, 10, anchor="ne", text="Time: 0", fill="white", font=("Arial", 12))

        # Start the game loop
        self.game_loop()

    def move_left(self, event):
        if not self.is_game_over:
            # Move the player left, ensuring it stays inside the screen bounds
            self.canvas.move(self.player, -20, 0)
            if self.canvas.coords(self.player)[0] < 0:  # Check if player is out of bounds
                self.canvas.move(self.player, 20, 0)  # Prevent going out of the left side

    def move_right(self, event):
        if not self.is_game_over:
            # Move the player right, ensuring it stays inside the screen bounds
            self.canvas.move(self.player, 20, 0)
            if self.canvas.coords(self.player)[2] > WIDTH:  # Check if player is out of bounds
                self.canvas.move(self.player, -20, 0)  # Prevent going out of the right side

    def create_falling_object(self):
        # Randomly create falling objects with random sizes
        x_pos = random.randint(20, WIDTH - 20)
        object_size = random.randint(15, 30)
        falling_object = self.canvas.create_oval(
            x_pos - object_size, 0,
            x_pos + object_size, object_size,
            fill="blue"
        )
        self.objects.append(falling_object)

    def move_objects(self):
        for obj in self.objects:
            # Move falling objects downward, increase speed over time for difficulty
            self.canvas.move(obj, 0, 5 + self.difficulty)
            if self.check_collision(obj):
                self.game_over()  # End the game on collision
            elif self.canvas.coords(obj)[3] > HEIGHT:
                self.canvas.delete(obj)
                self.objects.remove(obj)
                self.score += 1  # Increase score for surviving objects

    def check_collision(self, obj):
        # Get player coordinates
        player_coords = self.canvas.coords(self.player)
        player_x1, player_y1, player_x2, player_y2 = player_coords

        # Get object coordinates
        object_coords = self.canvas.coords(obj)
        object_x1, object_y1, object_x2, object_y2 = object_coords

        # Check for collision between the player and the falling object
        if (player_x1 < object_x2 and player_x2 > object_x1 and
            player_y1 < object_y2 and player_y2 > object_y1):
            return True
        return False

    def game_over(self):
        self.is_game_over = True
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="white", font=("Arial", 24))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 80, text="Press 'R' to Restart", fill="white", font=("Arial", 12))

    def game_loop(self):
        if not self.is_game_over:
            # Randomly create falling objects at a certain frequency
            if random.random() < 0.1:
                self.create_falling_object()

            # Move the objects and check for collisions
            self.move_objects()

            # Update the score display and timer
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            
            # Update timer: Calculate elapsed time
            elapsed_time = int(time.time() - self.start_time)
            self.canvas.itemconfig(self.timer_text, text=f"Time: {elapsed_time}")

            # Increase difficulty as time progresses
            if self.score % 50 == 0 and self.score > 0:
                self.difficulty += 0.2  # Increase falling speed

            # Update the game state every 1000/FPS milliseconds
            self.root.after(1000 // FPS, self.game_loop)
        else:
            self.root.bind("<r>", self.restart_game)

    def restart_game(self, event):
        # Restart the game
        self.canvas.delete("all")
        self.__init__(self.root)


# Create the Tkinter window and run the game
root = tk.Tk()
game = DodgeGame(root)
root.mainloop()
