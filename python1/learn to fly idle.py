import tkinter as tk
import random
import time
import json
import os

# Game Variables
money = 0
flight_power = 10
earn_rate = 1
upgrade_cost = 10
auto_fly = False
auto_fly_rate = 1  # Auto fly will add money per second
save_file = "game_save.json"  # File to save progress

# Load Game State (if exists)
def load_game():
    global money, flight_power, earn_rate, upgrade_cost, auto_fly
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            saved_data = json.load(f)
            money = saved_data.get("money", 0)
            flight_power = saved_data.get("flight_power", 10)
            earn_rate = saved_data.get("earn_rate", 1)
            upgrade_cost = saved_data.get("upgrade_cost", 10)
            auto_fly = saved_data.get("auto_fly", False)
        print("Game loaded!")
    else:
        print("No saved game found.")

# Save Game State
def save_game():
    global money, flight_power, earn_rate, upgrade_cost, auto_fly
    save_data = {
        "money": money,
        "flight_power": flight_power,
        "earn_rate": earn_rate,
        "upgrade_cost": upgrade_cost,
        "auto_fly": auto_fly
    }
    with open(save_file, "w") as f:
        json.dump(save_data, f)
    print("Game saved!")

# Game Functions
def update_money():
    global money
    money += earn_rate
    money_label.config(text=f"Money: ${money}")

def launch_bird():
    global money, flight_power
    if money >= flight_power:
        money -= flight_power
        flight_power = random.randint(15, 50)  # New flight power after launch
        money_label.config(text=f"Money: ${money}")
        flight_power_label.config(text=f"Flight Power: {flight_power}")
        print(f"Bird launched with flight power: {flight_power}")
    else:
        print("Not enough money to launch!")

def upgrade():
    global money, earn_rate, upgrade_cost
    if money >= upgrade_cost:
        money -= upgrade_cost
        earn_rate += 1
        upgrade_cost = int(upgrade_cost * 1.5)  # Increase the cost for the next upgrade
        money_label.config(text=f"Money: ${money}")
        earn_rate_label.config(text=f"Earn Rate: {earn_rate}/s")
        upgrade_cost_label.config(text=f"Upgrade Cost: ${upgrade_cost}")
        print(f"Upgrade purchased! Earn rate is now: {earn_rate}")
    else:
        print("Not enough money for upgrade!")

def start_auto_fly():
    global auto_fly
    auto_fly = True
    auto_fly_button.config(state=tk.DISABLED)  # Disable button once clicked
    print("Auto-Fly activated!")

def auto_fly_earn():
    global money
    if auto_fly:
        money += auto_fly_rate
        money_label.config(text=f"Money: ${money}")

# Tkinter Setup
root = tk.Tk()
root.title("Learn to Fly Idle Game")
root.geometry("800x600")  # Make the window bigger (Width: 800px, Height: 600px)
root.configure(bg="black")  # Set the background color of the window to black

# Load Game State
load_game()

# Labels for money, flight power, and earn rate (increase font size and change text color to white for contrast)
money_label = tk.Label(root, text=f"Money: ${money}", font=("Arial", 20), bg="black", fg="white")  # Increased font size to 24
money_label.pack(pady=20)

flight_power_label = tk.Label(root, text=f"Flight Power: {flight_power}", font=("Arial", 18), bg="black", fg="white")  # Increased font size to 20
flight_power_label.pack(pady=20)

earn_rate_label = tk.Label(root, text=f"Earn Rate: {earn_rate}/s", font=("Arial", 18), bg="black", fg="white")  # Increased font size to 20
earn_rate_label.pack(pady=20)

upgrade_cost_label = tk.Label(root, text=f"Upgrade Cost: ${upgrade_cost}", font=("Arial", 18), bg="black", fg="white")  # Increased font size to 20
upgrade_cost_label.pack(pady=20)

# Buttons for actions (increase font size and make buttons bigger)
launch_button = tk.Button(root, text="Launch Bird", font=("Arial", 18), command=launch_bird, bg="gray", fg="white", height=2, width=20)  # Larger font, height, and width
launch_button.pack(pady=20)

upgrade_button = tk.Button(root, text="Upgrade", font=("Arial", 18), command=upgrade, bg="gray", fg="white", height=2, width=20)  # Larger font, height, and width
upgrade_button.pack(pady=20)

auto_fly_button = tk.Button(root, text="Activate Auto-Fly", font=("Arial", 18), command=start_auto_fly, bg="gray", fg="white", height=2, width=20)  # Larger font, height, and width
auto_fly_button.pack(pady=20)


# Game Loop for Idle Earnings
def game_loop():
    update_money()  # Update money on the screen
    auto_fly_earn()  # Auto-fly adds money if active
    root.after(1000, game_loop)  # Run this function every 1 second

# Start the Game Loop
game_loop()

# Save the game when the window is closed
def on_closing():
    save_game()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start Tkinter Event Loop
root.mainloop()
