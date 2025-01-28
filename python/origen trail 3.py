class OriginTrailGame:  
    def __init__(self):  
        self.reset_game()  

    def print_slow(self, text, delay=0.05):  
        """Prints text slowly to create a more engaging experience."""  
        for char in text:  
            print(char, end='', flush=True)  
            time.sleep(delay)  
        print()  # Print a newline at the end  

    def introduction(self):  
        """Displays the introduction to the game."""  
        if os.path.exists("save_game.json"):  
            self.print_slow("Welcome back to the Oregon Trail!")  
            self.print_slow("Let's continue on your journey.")  
            self.load_game()  # Automatically load the game if a save file exists  
        else:  
            self.print_slow("Welcome to the Oregon Trail!")  
            self.print_slow("Your goal is to travel to Oregon, but be prepared for the challenges along the way.")  
            self.print_slow("You will face food shortages, sickness, and various other obstacles.")  
            self.print_slow("It will be challenging. Are you ready? Then let's get started on your journey!")  

    def reset_game(self):  
        """Resets the game state variables to the initial state."""  
        self.money = 200  
        self.inventory = {"Wood": 0, "Stone": 0, "Food": 0}  
        self.locations = ["Town", "Forest", "Mountain", "River", "Market"]  
        self.current_location = "Town"  
        self.day = 0  

    def load_game(self):  
        """Loads the game state from a file."""  
        if os.path.exists("save_game.json"):  
            with open("save_game.json", "r") as f:  
                game_state = json.load(f)  
                self.money = game_state["money"]  
                self.inventory = game_state["inventory"]  
                self.current_location = game_state["current_location"]  
                self.day = game_state["day"]  
            print("\nGame loaded successfully.")  
        else:  
            print("No saved game found.")  

    def play(self):  
        """Main loop for the game that allows user interaction."""  
        self.introduction()  # Call the introduction method before starting the game  

        while True:  
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

            choice = input("Enter your choice NOWW (1-9): ")  

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
            else:  
                print("WRONG! That's not a valid choice.")  

# Run the game  
if __name__ == "__main__":  
    game = OriginTrailGame()  
    game.play()  
