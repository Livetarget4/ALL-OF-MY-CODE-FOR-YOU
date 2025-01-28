import tkinter as tk

class ChaseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Player vs CPU - Chase Game")

        # Set up the game window
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightblue')
        self.canvas.pack()

        # Create the player (red rectangle)
        self.player = self.canvas.create_rectangle(100, 100, 150, 150, fill="red")

        # Create the CPU (green rectangle)
        self.cpu = self.canvas.create_rectangle(600, 400, 650, 450, fill="green")

        # Player's speed (increased to 10 for faster movement)
        self.speed = 10  # Player moves faster now

        # Player's position
        self.player_pos = {'x': 100, 'y': 100}

        # CPU's speed
        self.cpu_speed = 3

        # CPU's position
        self.cpu_pos = {'x': 600, 'y': 400}

        # Bind keys to control the player
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)

        # Start the game loop
        self.update()

    def move_left(self, event):
        """Move the player left"""
        self.player_pos['x'] -= self.speed

    def move_right(self, event):
        """Move the player right"""
        self.player_pos['x'] += self.speed

    def move_up(self, event):
        """Move the player up"""
        self.player_pos['y'] -= self.speed

    def move_down(self, event):
        """Move the player down"""
        self.player_pos['y'] += self.speed

    def cpu_move(self):
        """Make the CPU move towards the player"""
        # Get the current position of the player and CPU
        player_x, player_y = self.player_pos['x'], self.player_pos['y']
        cpu_x, cpu_y = self.cpu_pos['x'], self.cpu_pos['y']
        
        # Calculate the difference in position
        delta_x = player_x - cpu_x
        delta_y = player_y - cpu_y

        # Normalize the movement (to avoid faster diagonal movement)
        distance = (delta_x**2 + delta_y**2) ** 0.5
        if distance != 0:
            delta_x /= distance
            delta_y /= distance

        # Move the CPU towards the player
        self.cpu_pos['x'] += self.cpu_speed * delta_x
        self.cpu_pos['y'] += self.cpu_speed * delta_y

    def update(self):
        """Game loop to update the positions of the player and CPU"""
        # Move the player on the canvas
        self.canvas.coords(self.player, self.player_pos['x'], self.player_pos['y'], 
                           self.player_pos['x'] + 50, self.player_pos['y'] + 50)

        # Move the CPU on the canvas
        self.canvas.coords(self.cpu, self.cpu_pos['x'], self.cpu_pos['y'], 
                           self.cpu_pos['x'] + 50, self.cpu_pos['y'] + 50)

        # Make the CPU chase the player
        self.cpu_move()

        # Continue the game loop (60 FPS)
        self.root.after(16, self.update)  # ~60 FPS

# Create the main Tkinter window
root = tk.Tk()

# Initialize the game
game = ChaseGame(root)

# Start the Tkinter event loop
root.mainloop()
