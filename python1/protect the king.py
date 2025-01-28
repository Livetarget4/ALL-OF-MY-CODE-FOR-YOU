import tkinter as tk  
import random  

# Set up the main window  
root = tk.Tk()  
root.title("Save The King")  
root.geometry("400x600")  

# Game parameters  
player_size = 50  
player_speed = 9  # Speed of player movement  
projectile_size = 10  
enemy_size = 30  
enemy_speed = 5  
enemy_creation_interval = 2000  # Create a new enemy every 2 seconds  
projectile_speed = 10  

# Player positions and game state  
player1_x = 175  
player1_y = 490  
player2_x = 175  # Position for the second player  
player2_y = 550  
player_score = 0  
game_running = True  

# Lists for projectiles and enemies  
projectiles = []  
enemies = []  

# Set up the canvas  
canvas = tk.Canvas(root, width=400, height=600, bg="black")  
canvas.pack()  

# Flags for key press states (for continuous movement)  
move_left_flag = False  
move_right_flag = False  
move_up_flag = False  
move_down_flag = False  

# Function to start the game  
def start_game():  
    global game_running, player1_x, player1_y, projectiles, enemies, player_score  
    game_running = True  
    player1_x = 175  
    player1_y = 490  
    projectiles = []  
    enemies = []  
    player_score = 0  
    canvas.delete("all")  # Clear the canvas  
    root.after(100, create_enemy)  
    update_game()  

# Function to move the player based on key flags  
def move_player():  
    global player1_x, player1_y  
    if move_left_flag and player1_x > 0:  
        player1_x -= player_speed  
    if move_right_flag and player1_x < (root.winfo_width() - player_size):  
        player1_x += player_speed  
    if move_up_flag and player1_y > 0:  
        player1_y -= player_speed  
    if move_down_flag and player1_y < (root.winfo_height() - player_size):  
        player1_y += player_speed  
    draw()  

# Functions for key bindings to set flags  
def move_left(event):  
    global move_left_flag  
    move_left_flag = True  

def move_right(event):  
    global move_right_flag  
    move_right_flag = True  

def move_up(event):  
    global move_up_flag  
    move_up_flag = True  

def move_down(event):  
    global move_down_flag  
    move_down_flag = True  

def stop_left(event):  
    global move_left_flag  
    move_left_flag = False  

def stop_right(event):  
    global move_right_flag  
    move_right_flag = False  

def stop_up(event):  
    global move_up_flag  
    move_up_flag = False  

def stop_down(event):  
    global move_down_flag  
    move_down_flag = False  

# Function to shoot a projectile  
def shoot(event):  
    if game_running:  
        projectile_x = player1_x + player_size // 2 - projectile_size // 2  
        projectile_y = player1_y  
        projectiles.append([projectile_x, projectile_y])  
        draw()  

# Function to create a new enemy  
def create_enemy():  
    if not game_running:  
        return  
    canvas_width = canvas.winfo_width()  
    x_position = random.randint(0, canvas_width - enemy_size)  
    enemies.append([x_position, 0])  
    root.after(enemy_creation_interval, create_enemy)  

# Function to update the game state (move projectiles, enemies, check collisions)  
def update_game():  
    global game_running, player_score, projectiles, enemies  
    if not game_running:  
        return  
    move_player()  

    # Move projectiles  
    for proj in projectiles[:]:  
        proj[1] -= projectile_speed  # Move projectile upwards  
        if proj[1] < 0:  # Remove projectiles that are off the screen  
            projectiles.remove(proj)  
    
    # Move enemies downwards  
    for enemy in enemies[:]:  
        enemy[1] += enemy_speed  # Move enemy down  
        if enemy[1] > root.winfo_height():  # Enemy has passed the bottom  
            enemies.remove(enemy)  
            global player_score  
            player_score -= 1  # Lose 1 point when an enemy hits the bottom  

    # Collision detection with player 1  
    for enemy in enemies[:]:  
        if (enemy[1] + enemy_size >= player1_y and player1_x < enemy[0] + enemy_size and player1_x + player_size > enemy[0]):    
            player_score -= 1
            
    for enemy in enemies[:]:  
        if (enemy[1] + enemy_size >= player2_y and player2_x < enemy[0] + enemy_size and player2_x + player_size > enemy[0]):  
            game_over()

    # Check for collisions between projectiles and enemies  
    for proj in projectiles[:]:  
        for enemy in enemies[:]:  
            if (proj[0] < enemy[0] + enemy_size and proj[0] + projectile_size > enemy[0] and proj[1] < enemy[1] + enemy_size and proj[1] + projectile_size > enemy[1]):  
                projectiles.remove(proj)  # Remove the projectile  
                enemies.remove(enemy)  # Remove the enemy  
                player_score += 1  # Increase score  
    
    draw()  
    root.after(20, update_game)  

# Function to draw everything on the canvas  
def draw():  
    canvas.delete("all")  # Clear the previous drawing  
    # Draw player 1  
    canvas.create_rectangle(player1_x, player1_y, player1_x + player_size, player1_y + player_size, fill="gray")  
    # Draw player 2 (static)  
    canvas.create_rectangle(player2_x, player2_y, player2_x + player_size, player2_y + player_size, fill="yellow")  # Color changed to green for differentiation  
    # Draw projectiles  
    for proj in projectiles:  
        canvas.create_rectangle(proj[0], proj[1], proj[0] + projectile_size, proj[1] + projectile_size, fill="yellow")  
    # Draw enemies  
    for enemy in enemies:
        canvas.create_rectangle(enemy[0], enemy[1], enemy[0] + enemy_size, enemy[1] + enemy_size, fill="red")
    # Draw the score
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {player_score}", font=("Arial", 12), fill="white")

# Game Over screen
def game_over():
    global game_running
    game_running = False  # Stop the game
    canvas.delete("all")
    canvas.create_text(root.winfo_width() // 2, root.winfo_height() // 3, text="Game Over!", font=("Arial", 24), fill="red")
    canvas.create_text(root.winfo_width() // 2, root.winfo_height() // 2, text=f"Score: {player_score}", font=("Arial", 18), fill="black")
    restart_button = tk.Button(root, text="Restart", command=start_game)
    restart_button.pack()
    
# Bind keys to control the player
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)
root.bind("<space>", shoot)  # Spacebar to shoot

# Bind keys to stop movement when the key is released
root.bind("<KeyRelease-Left>", stop_left)
root.bind("<KeyRelease-Right>", stop_right)
root.bind("<KeyRelease-Up>", stop_up)
root.bind("<KeyRelease-Down>", stop_down)

# Start the game
start_game()

# Start the main loop
root.mainloop()
