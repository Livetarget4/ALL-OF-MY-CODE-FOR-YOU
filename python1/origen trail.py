import random
import time

# Game Class
class OriginTrailGame:
    def __init__(self):
        # Starting state
        self.money = 200
        self.resources = {"Wood": 0, "Stone": 0, "Food": 0}
        self.inventory = {"Wood": 0, "Stone": 0, "Food": 0}
        self.locations = ["Town", "Forest", "Mountain", "River", "Market"]
        self.current_location = "Town"
        self.day = 0

    def display_status(self):
        print(f"\nDay {self.day} - Current Location: {self.current_location}")
        print(f"Money: ${self.money}")
        print("Resources in inventory:")
        for resource, amount in self.inventory.items():
            print(f"  {resource}: {amount}")
        print()

    def gather_resources(self):
        # Gathering resources based on the current location
        if self.current_location == "Forest":
            resource = "Wood"
        elif self.current_location == "Mountain":
            resource = "Stone"
        elif self.current_location == "River":
            resource = "Food"
        else:
            print("No resources to gather here.")
            return

        amount = random.randint(1, 5)
        self.inventory[resource] += amount
        print(f"You gathered {amount} {resource}.")
        
    def trade_resources(self):
        # Trade resources at the market for money
        if self.current_location != "Market":
            print("You need to go to the market to trade.")
            return
        
        print("Trading your resources for money...")
        trade_amount = random.randint(1, 3)
        trade_value = 10 * trade_amount  # Each trade item is worth $10
        if self.inventory["Wood"] >= trade_amount:
            self.inventory["Wood"] -= trade_amount
            self.money += trade_value
            print(f"Traded {trade_amount} Wood for ${trade_value}.")
        else:
            print("Not enough Wood to trade.")
        
    def explore(self):
        print("\nExploring...")
        # Randomly choose a new location
        self.current_location = random.choice(self.locations)
        print(f"Moved to {self.current_location}.")
        
    def next_day(self):
        self.day += 1
        time.sleep(1)

    def play(self):
        print("Welcome to Origin Trail - A simple resource management game!")
        
        while True:
            self.display_status()
            
            print("What would you like to do?")
            print("1. Gather Resources")
            print("2. Trade Resources")
            print("3. Explore")
            print("4. End Game")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                self.gather_resources()
            elif choice == "2":
                self.trade_resources()
            elif choice == "3":
                self.explore()
            elif choice == "4":
                print("WOW YOUR LEAVING JUST WOW")
            else:
                print("WROUNG THATS NOT A CHOCIE DUMB DUMB")
            
            self.next_day()

# Run the game
if __name__ == "__main__":
    game = OriginTrailGame()
    game.play()
