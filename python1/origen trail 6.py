import random  
import time  
import json  
import os  

class OriginTrailGame:  
    def __init__(self):  
        self.reset_game()
        # Add new attributes
        self.health = 100
        self.energy = 100
        self.weather_conditions = ["Sunny", "Rainy", "Stormy", "Snowy"]
        self.current_weather = "Sunny"

    def print_slow(self, text, delay=0.05):  
        """Prints text slowly to create a more engaging experience."""  
        for char in text:  
            print(char, end='', flush=True)  
            time.sleep(delay)  
        print()  # Print a newline at the end  

    def introduction(self):  
        """Displays the introduction to the game."""  
        self.print_slow("Welcome to the Oregon Trail!")  
        self.print_slow("Your goal is to travel to Oregon, but be prepared for the challenges along the way.")  
        self.print_slow("You will face food shortages, sickness, and various other obstacles.")
        self.print_slow("It will be challenging are you ready then lets get started on your journey")  
    
    def reset_game(self):  
        """Resets the game state variables to the initial state."""  
        self.money = 200  
        self.inventory = {"Wood": 0, "Stone": 0, "Food": 0}  
        self.locations = ["Town", "Forest", "Mountain", "River", "Market"]  
        self.current_location = "Town"  
        self.day = 0  
        # Add new reset values
        self.health = 100
        self.energy = 100
        self.current_weather = "Sunny"

    def display_status(self):  
        """Displays the current status of the game."""  
        print(f"\nDay {self.day} - Current Location: {self.current_location}")  
        print(f"Money: ${self.money}")  
        print("Resources in inventory:")  
        for resource, amount in self.inventory.items():  
            print(f"  {resource}: {amount}")  
        print(f"Health: {self.health}%")
        print(f"Energy: {self.energy}%")
        print(f"Weather: {self.current_weather}")
        print()  

    def update_weather(self):
        """Randomly changes the weather condition."""
        self.current_weather = random.choice(self.weather_conditions)
        self.print_slow(f"The weather has changed to {self.current_weather}!")
        
        # Weather effects
        if self.current_weather == "Stormy":
            damage = random.randint(5, 15)
            self.health -= damage
            self.print_slow(f"The storm caused {damage} damage to your health!")
        elif self.current_weather == "Snowy":
            energy_loss = random.randint(10, 20)
            self.energy -= energy_loss
            self.print_slow(f"The cold weather drained {energy_loss} energy!")

    def rest(self):
        """Allow the player to rest and recover energy/health."""
        energy_gain = random.randint(20, 40)
        health_gain = random.randint(10, 25)
        
        self.energy = min(100, self.energy + energy_gain)
        self.health = min(100, self.health + health_gain)
        
        self.print_slow(f"You rested and recovered {energy_gain} energy and {health_gain} health!")
        self.next_day()

    def check_game_over(self):
        """Check if the player has lost the game."""
        if self.health <= 0:
            self.print_slow("Your health has reached 0! Game Over!")
            return True
        elif self.energy <= 0:
            self.print_slow("Your energy has been depleted! Game Over!")
            return True
        return False

    def gather_resources(self):  
        """Gathers resources based on the current location."""  
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
        """Trades resources at the market for money."""  
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

    def add_money(self):  
        """Adds money to the player's balance."""  
        amount = random.randint(50, 100)  
        self.money += amount  
        print(f"You found ${amount} on the ground!")  

    def shop(self):  
        """Displays shop options and allows buying/selling resources."""  
        print("\nWelcome to the Shop!")  
        shop_prices = {"Wood": 15, "Stone": 20, "Food": 10}  # Prices for buying resources  
        sell_prices = {"Wood": 5, "Stone": 10, "Food": 3}  # Prices for selling resources  

        while True:  
            print("\nAvailable resources in the shop:")  
            for resource, price in shop_prices.items():  
                print(f"{resource}: ${price} each")  
            print("\nYour inventory:")  
            for resource, amount in self.inventory.items():  
                print(f"  {resource}: {amount}")  

            print("\nWhat would you like to do?")  
            print("1. Buy Resources")  
            print("2. Sell Resources")  
            print("3. Exit Shop")  

            choice = input("Enter your choice (1-3): ")  

            if choice == "1":  
                resource = input("Enter the resource you want to buy (Wood, Stone, Food): ").capitalize()  
                if resource in shop_prices:  
                    amount = int(input("Enter the amount you want to buy: "))  
                    total_cost = shop_prices[resource] * amount  
                    if self.money >= total_cost:  
                        self.money -= total_cost  
                        self.inventory[resource] += amount  
                        print(f"Bought {amount} {resource} for ${total_cost}.")  
                    else:  
                        print("Not enough money to buy that resource.")  
                else:  
                    print("Invalid resource.")  

            elif choice == "2":  
                resource = input("Enter the resource you want to sell (Wood, Stone, Food): ").capitalize()  
                if resource in sell_prices and self.inventory[resource] > 0:  
                    amount = int(input("Enter the amount you want to sell: "))  
                    if self.inventory[resource] >= amount:  
                        total_value = sell_prices[resource] * amount  
                        self.inventory[resource] -= amount  
                        self.money += total_value  
                        print(f"Sold {amount} {resource} for ${total_value}.")  
                    else:  
                        print("Not enough of that resource to sell.")  
                else:  
                    print("Invalid resource or you have none.")  

            elif choice == "3":  
                print("Exiting shop.")  
                break  
            else:  
                print("Invalid choice. Please choose again.")  

    def travel(self):  
        """Allows the user to travel to different locations."""  
        print("\nAvailable locations to travel to:")  
        for idx, location in enumerate(self.locations, start=1):  
            print(f"{idx}. {location}")  

        choice = input("Choose a location to travel to (1-5): ")  
        if choice.isdigit() and 1 <= int(choice) <= len(self.locations):  
            self.current_location = self.locations[int(choice) - 1]  
            print(f"You traveled to {self.current_location}.")  
        else:  
            print("Invalid choice. Please choose a valid location.")  

    def next_day(self):  
        """Advances the game by one day."""  
        self.day += 1  
        time.sleep(1)  

    def save_game(self):  
        """Saves the game state to a file."""  
        game_state = {  
            "money": self.money,  
            "inventory": self.inventory,  
            "current_location": self.current_location,  
            "day": self.day,
            "health": self.health,
            "energy": self.energy,
            "current_weather": self.current_weather
        }  
        with open("save_game.json", "w") as f:  
            json.dump(game_state, f)  
        print("YAY YOU SAVED ME")  

    def load_game(self):  
        """Loads the game state from a file."""  
        if os.path.exists("save_game.json"):  
            with open("save_game.json", "r") as f:  
                game_state = json.load(f)  
                self.money = game_state["money"]  
                self.inventory = game_state["inventory"]  
                self.current_location = game_state["current_location"]  
                self.day = game_state["day"]
                self.health = game_state.get("health", 100)
                self.energy = game_state.get("energy", 100)
                self.current_weather = game_state.get("current_weather", "Sunny")
            print("YAY YOU LOADED ME")  
        else:  
            print("No saved game found.")  

    def play(self):  
        """Main loop for the game that allows user interaction."""  
        self.introduction()  

        while True:  
            if self.check_game_over():
                break

            self.display_status()  

            print("What would you like to do?")  
            print("1. Gather Resources")  
            print("2. Trade Resources")  
            print("3. Visit Shop")  
            print("4. Travel")  
            print("5. Save Game")  
            print("6. Load Game")  
            print("7. Restart Game")  
            print("8. End Game")  
            print("9. Add Money")
            print("10. Rest")
            print("11. Check Weather")  

            choice = input("Enter your choice NOWW (1-11): ")  

            if choice == "1":  
                self.gather_resources()  
                self.next_day()
            elif choice == "2":  
                self.trade_resources()  
                self.next_day()
            elif choice == "3":  
                self.shop()
            elif choice == "4":  
                self.travel()  
                self.next_day()
            elif choice == "5":  
                self.save_game()  
            elif choice == "6":  
                self.load_game()  
            elif choice == "7":  
                self.reset_game()
            elif choice == "8":  
                print("Thanks for playing!")  
                break  
            elif choice == "9":  
                self.add_money()
            elif choice == "10":
                self.rest()
            elif choice == "11":
                self.update_weather()
            else:  
                print("WROUNG THATS NOT A CHOICE DUMB DUMB")

            # Random weather changes
            if random.random() < 0.2:  # 20% chance of weather change each turn
                self.update_weather()

# Run the game  
if __name__ == "__main__":  
    game = OriginTrailGame()  
    game.load_game()  # Load the game at the start  
    game.play()
