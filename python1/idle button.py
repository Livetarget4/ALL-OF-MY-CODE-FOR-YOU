import tkinter as tk
import json
import os

# Game Variables
money = 0
money_per_click = 1
earn_rate = 0  # For automatic earnings
upgrade_cost = 10
auto_earn_rate = 1  # Rate of automatic money earning per second
save_file = "game_save.json"  # File to save progress

# Load Game State (if exists)
def load_game():
    global money, money_per_click, earn_rate, upgrade_cost, auto_earn_rate
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            saved_data = json.load(f)
            money = saved_data.get("money", 0)
            money_per_click = saved_data.get("money_per_click", 1)
            earn_rate = saved_data.get("earn_rate", 0)
            upgrade_cost = saved_data.get("upgrade_cost", 10)
            auto_earn_rate = saved_data.get("auto_earn_rate", 1)
        print("Game loaded!")
    else:
        print("No saved game found.")

# Save Game State
def save_game():
    global money, money_per_click, earn_rate, upgrade_cost, auto_earn_rate
    save_data = {
        "money": money,
        "money_per_click": money_per_click,
        "earn_rate": earn_rate,
        "upgrade_cost": upgrade_cost,
        "auto_earn_rate": auto_earn_rate
    }
    with open(save_file, "w") as f:
        json.dump(save_data, f)
    print("Game saved!")

# Game Functions
def earn_money():
    global money
    money += money_per_click
    update_labels()

def upgrade():
    global money, money_per_click, upgrade_cost
    if money >= upgrade_cost:
        money -= upgrade_cost
        money_per_click += 1
        upgrade_cost = int(upgrade_cost * 1.5)  # Increase the cost for the next upgrade
        update_labels()
        print(f"Upgrade purchased! Money per click: {money_per_click}")
    else:
        print("Not enough money to upgrade!")

def start_auto_earn():
    global earn_rate
    earn_rate = auto_earn_rate
    auto_earn_button.config(state=tk.DISABLED)  # Disable button after clicking
    print("Automatic earning started!")

def auto_earn():
    global money
    if earn_rate > 0:
        money += earn_rate
        update_labels()

def update_labels():
    money_label.config(text=f"Money: ${money}")
    money_per_click_label.config(text=f"Money per click: {money_per_click}")
    upgrade_cost_label.config(text=f"Upgrade Cost: ${upgrade_cost}")

# Tkinter Setup
root = tk.Tk()
root.title("Idle Button Game")
root.geometry("600x400")
root.configure(bg="black")  # Set background color

# Load Game State
load_game()

# Labels for money and upgrades
money_label = tk.Label(root, text=f"Money: ${money}", font=("Arial", 20), bg="black", fg="white")
money_label.pack(pady=10)

money_per_click_label = tk.Label(root, text=f"Money per click: {money_per_click}", font=("Arial", 16), bg="black", fg="white")
money_per_click_label.pack(pady=10)

upgrade_cost_label = tk.Label(root, text=f"Upgrade Cost: ${upgrade_cost}", font=("Arial", 16), bg="black", fg="white")
upgrade_cost_label.pack(pady=10)

# Buttons for actions
earn_button = tk.Button(root, text="Earn Money", font=("Arial", 16), command=earn_money, bg="gray", fg="white", height=2, width=20)
earn_button.pack(pady=10)

upgrade_button = tk.Button(root, text="Upgrade Money per Click", font=("Arial", 16), command=upgrade, bg="gray", fg="white", height=2, width=20)
upgrade_button.pack(pady=10)

auto_earn_button = tk.Button(root, text="Start Auto Earn", font=("Arial", 16), command=start_auto_earn, bg="gray", fg="white", height=2, width=20)
auto_earn_button.pack(pady=10)

# Game Loop for Auto Earnings
def game_loop():
    auto_earn()  # Automatically earn money over time
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
