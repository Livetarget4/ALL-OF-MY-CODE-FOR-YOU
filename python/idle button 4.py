import tkinter as tk
import random
import winsound  # For adding sound effects (only works on Windows)

# Game Variables
score = 0
points_per_click = 1
upgrade_cost = 10
auto_clicker_cost = 100
upgrade_multiplier = 1.5  # Used for upgrade cost scaling
is_game_started = False
high_score = 0

# Game Functions
def click_button():
    global score
    score += points_per_click
    score_label.config(text=f"Score: {score}")
    play_click_sound()

def upgrade_button():
    global score, points_per_click, upgrade_cost
    if score >= upgrade_cost:
        score -= upgrade_cost
        points_per_click += 1
        upgrade_cost = int(upgrade_cost * upgrade_multiplier)  # Increase cost for next upgrade
        score_label.config(text=f"Score: {score}")
        upgrade_cost_label.config(text=f"Upgrade Cost: {upgrade_cost}")
        points_per_click_label.config(text=f"Points per Click: {points_per_click}")
        play_upgrade_sound()
    else:
        play_error_sound()

def buy_auto_clicker():
    global score, auto_clicker_cost
    if score >= auto_clicker_cost:
        score -= auto_clicker_cost
        score_label.config(text=f"Score: {score}")
        play_auto_clicker_sound()
        start_auto_clicker()

def start_auto_clicker():
    """Automatically add points every second."""
    global score
    score += points_per_click
    score_label.config(text=f"Score: {score}")
    root.after(1000, start_auto_clicker)  # Repeat every 1000ms (1 second)

def play_click_sound():
    """Play sound effect on button click."""
    winsound.Beep(1000, 200)  # Beep sound on click (Frequency, Duration)

def play_upgrade_sound():
    """Play sound effect when upgrading."""
    winsound.Beep(1500, 300)  # Different beep sound for upgrade

def play_error_sound():
    """Play error sound when upgrade can't be afforded."""
    winsound.Beep(500, 300)  # Error beep sound for insufficient funds

def play_auto_clicker_sound():
    """Play sound when auto-clicker is purchased."""
    winsound.Beep(2000, 400)  # A pleasant beep when the auto-clicker is purchased


# Tkinter Setup
root = tk.Tk()
root.title("Button Clicking Game")
root.geometry("600x600")
root.configure(bg="#333333")  # Dark background color

# Start Screen
start_screen = tk.Frame(root, bg="#333333")
start_screen.pack(fill=tk.BOTH, expand=True)

start_label = tk.Label(start_screen, text="Welcome to the Button Clicking Game", font=("Arial", 50, "bold"), bg="#333333", fg="white")
start_label.pack(pady=20)

# Start Game Button with animation
start_button = tk.Button(start_screen, text="Start Game", font=("Arial", 40, "bold"), command=start_game, bg="#FF5722", fg="black", height=2, width=20)

# Animate the "Start Game" Button (changing color and size)
def animate_start_button():
    colors = ["#FF5722", "#FF9800", "#4CAF50", "#2196F3", "#9C27B0"]
    current_color = start_button.cget("bg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]  # Change color in a loop
    start_button.config(bg=next_color, font=("Arial", 50, "bold"))  # Slightly increase font size with each loop
    start_button.after(500, animate_start_button)  # Repeat every 500ms

# Start animating the button when the program starts
animate_start_button()

start_button.pack(pady=20)

# Game Screen
game_screen = tk.Frame(root, bg="#333333")

# Labels for game screen
score_label = tk.Label(game_screen, text=f"Score: {score}", font=("Arial", 40), bg="#333333", fg="white")
score_label.pack(pady=10)

points_per_click_label = tk.Label(game_screen, text=f"Points per Click: {points_per_click}", font=("Arial", 30), bg="#333333", fg="white")
points_per_click_label.pack(pady=10)

upgrade_cost_label = tk.Label(game_screen, text=f"Upgrade Cost: {upgrade_cost}", font=("Arial", 30), bg="#333333", fg="white")
upgrade_cost_label.pack(pady=10)

auto_clicker_cost_label = tk.Label(game_screen, text=f"Auto Clicker Cost: {auto_clicker_cost}", font=("Arial", 30), bg="#333333", fg="white")
auto_clicker_cost_label.pack(pady=10)

# Buttons for game screen
click_button_button = tk.Button(game_screen, text="Click Me!", font=("Arial", 30), command=click_button, bg="#FF5722", fg="black", height=2, width=20)

# Animate the "Click Me!" Button (changing color and size)
def animate_click_button():
    colors = ["#FF5722", "#FF9800", "#4CAF50", "#2196F3", "#9C27B0"]
    current_color = click_button_button.cget("bg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]  # Change color in a loop
    click_button_button.config(bg=next_color, font=("Arial", 30, "bold"))  # Slightly increase font size with each loop
    click_button_button.after(500, animate_click_button)  # Repeat every 500ms

# Start animating the "Click Me!" button when the game starts
animate_click_button()

click_button_button.pack(pady=10)

upgrade_button_button = tk.Button(game_screen, text="Upgrade Button", font=("Arial", 30), command=upgrade_button, bg="#FF9800", fg="black", height=2, width=20)
upgrade_button_button.pack(pady=10)

auto_clicker_button = tk.Button(game_screen, text="Buy Auto Clicker", font=("Arial", 30), command=buy_auto_clicker, bg="#4CAF50", fg="black", height=2, width=20)
auto_clicker_button.pack(pady=10)

# Start Tkinter Event Loop
root.mainloop()
