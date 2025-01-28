import tkinter as tk

# Game Variables
score = 0
points_per_click = 1
upgrade_cost = 10
is_game_started = False  # Flag to track whether the game has started

# Game Functions
def click_button():
    global score
    score += points_per_click
    score_label.config(text=f"Score: {score}")

def upgrade_button():
    global score, points_per_click, upgrade_cost
    if score >= upgrade_cost:
        score -= upgrade_cost
        points_per_click += 1
        upgrade_cost = int(upgrade_cost * 1.5)  # Increase cost for next upgrade
        score_label.config(text=f"Score: {score}")
        upgrade_cost_label.config(text=f"Upgrade Cost: {upgrade_cost}")
        points_per_click_label.config(text=f"Points per Click: {points_per_click}")
        print(f"Upgrade purchased! Points per click: {points_per_click}")
    else:
        print("Not enough score to upgrade!")

def game_over():
    global score
    click_button_button.config(state=tk.DISABLED)  # Disable the click button
    upgrade_button_button.config(state=tk.DISABLED)  # Disable upgrade button
    game_over_label.config(text=f"Game Over! Your final score is: {score}")

def start_game():
    global is_game_started
    if not is_game_started:
        is_game_started = True
        start_screen.pack_forget()  # Hide the start screen
        game_screen.pack(fill=tk.BOTH, expand=True)  # Show the game screen
        print("Game Started!")

# Tkinter Setup
root = tk.Tk()
root.title("Button Clicking Game")
root.geometry("600x600")
root.configure(bg="black")  # Set background color

# Start Screen
start_screen = tk.Frame(root, bg="black")
start_screen.pack(fill=tk.BOTH, expand=True)

start_label = tk.Label(start_screen, text="Welcome to the Button Clicking Game", font=("Arial", 50), bg="black", fg="white")
start_label.pack(pady=20)

# Start Game Button
start_button = tk.Button(start_screen, text="Start Game", font=("Arial", 60), command=start_game, bg="teal", fg="black", height=2, width=20)

# Animate the "Start Game" Button (changing color and size)
def animate_start_button():
    colors = ["teal", "blue", "green", "red", "purple"]
    current_color = start_button.cget("bg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]  # Change color in a loop
    start_button.config(bg=next_color, font=("Arial", 60 + (score % 5)))  # Slightly increase font size with each loop
    start_button.after(500, animate_start_button)  # Repeat every 500ms

# Start animating the button when the program starts
animate_start_button()

start_button.pack(pady=20)

# Game Screen
game_screen = tk.Frame(root, bg="black")

# Labels for game screen
score_label = tk.Label(game_screen, text=f"Score: {score}", font=("Arial", 40), bg="black", fg="white")
score_label.pack(pady=10)

points_per_click_label = tk.Label(game_screen, text=f"Points per Click: {points_per_click}", font=("Arial", 40), bg="black", fg="white")
points_per_click_label.pack(pady=10)

upgrade_cost_label = tk.Label(game_screen, text=f"Upgrade Cost: {upgrade_cost}", font=("Arial", 40), bg="black", fg="white")
upgrade_cost_label.pack(pady=10)

# Buttons for game screen
click_button_button = tk.Button(game_screen, text="Click Me!", font=("Arial", 30), command=click_button, bg="teal", fg="gray", height=2, width=20)

# Animate the "Click Me!" Button (changing color and size)
def animate_click_button():
    colors = ["teal", "blue", "green", "red", "purple"]
    current_color = click_button_button.cget("bg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]  # Change color in a loop
    click_button_button.config(bg=next_color, font=("Arial", 30 + (score % 5)))  # Slightly increase font size with each loop
    click_button_button.after(500, animate_click_button)  # Repeat every 500ms

# Start animating the "Click Me!" button when the game starts
animate_click_button()

click_button_button.pack(pady=10)

upgrade_button_button = tk.Button(game_screen, text="Upgrade Button", font=("Arial", 30), command=upgrade_button, bg="gray", fg="white", height=2, width=20)
upgrade_button_button.pack(pady=10)

# Start Tkinter Event Loop
root.mainloop()
