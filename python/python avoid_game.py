import tkinter as tk
import random

# Set up the main window
root = tk.Tk()
root.title("Avoid Falling Objects Game")
root.geometry("400x600")

# Game parameters
player_size = 50
object_size = 30
player_speed = 20
object_speed = 2
object_creation_interval = 2000  # Create a new object every 2 seconds

# Player position and game state
player_x = 175
player_y = 550
falling_objects = []
game_running = False
score = 0

# Set up the canvas
canvas = tk.Canvas(root, width=400, height=600, bg="white")
canvas.pack()

# Function to start the game
def start_game():
    global game_running
    game_running = True
    create_object()  # Start creating falling objects
    update_objects()  # Start the game loop to update falling objects

# Function to create a new falling object
def create_object():
    if not game_running:
        return
    # Randomly place the object within the canvas width
    x_position = random.randint(0, root.winfo_width() - object_size)
    falling_objects.append([x_position, 0])  # Object starts at the top (y=0)
    root.after(object_creation_interval, create_object)  # Recurse to create more objects

# Function to move the player
def move_left(event):
    global player_x
    if player_x > 0:
        player_x -= player_speed
    draw()

def move_right(event):
    global player_x
    if player_x < (root.winfo_width() - player_size):
        player_x += player_speed
    draw()

# Function to update the falling objects
def update_objects():
    global falling_objects, object_speed, score, game_running
    if not game_running:
        return

    # Move each falling object down
    for obj in falling_objects[:]:
        obj[1] += object_speed  # Move object downwards
        if obj[1] > root.winfo_height():  # Remove objects that go off the screen
            falling_objects.remove(obj)
            score += 1  # Increase score for surviving objects

        # Collision detection
        if (obj[1] + object_size >= player_y and
            player_x < obj[0] + object_size and player_x + player_size > obj[0]):
            game_over()  # End game if collision occurs
            return

    draw()

# Function to draw everything on the canvas
def draw():
    canvas.delete("all")  # Clear the previous drawing

    # Draw the player
    canvas.create_rectangle(player_x, player_y, player_x + player_size, player_y + player_size, fill="blue")  

    # Draw the falling objects (enemies)
    for obj in falling_objects:
        canvas.create_rectangle(obj[0], obj[1], obj[0] + object_size, obj[1] + object_size, fill="red")  # Draw each object as red

    # Draw the score
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 12), fill="black")

    # Call the update_objects function to keep moving objects
    root.after(20, update_objects)

# Game Over screen
def game_over():
    global game_running, score
    game_running = False  # Stop the game loop
    canvas.delete("all")
    canvas.create_text(root.winfo_width() // 2, root.winfo_height() // 3, text="Game Over!", font=("Arial", 24), fill="red")
    canvas.create_text(root.winfo_width() // 2, root.winfo_height() // 2, text=f"Score: {score}", font=("Arial", 18), fill="black")
    restart_button = tk.Button(root, text="Restart", command=restart_game)
    restart_button.pack()

# Restart the game
def restart_game():
    global game_running, score, player_x, falling_objects
    score = 0
    player_x = 175
    falling_objects = []
    game_running = True
    canvas.delete("all")
    start_game()

# Start screen with Start Button
def start_screen():
    canvas.delete("all")
    canvas.create_text(root.winfo_width() // 2, root.winfo_height() // 3, text="Avoid Falling Objects", font=("Arial", 24), fill="black")
    start_button = tk.Button(root, text="Start", command=start_game)
    start_button.pack()

# Bind keys to move the player
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Show the start screen when the app opens
start_screen()

# Start the main loop
root.mainloop()
