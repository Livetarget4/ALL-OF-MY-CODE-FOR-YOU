import random
import time

class OregonTrailGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.party_health = 100
        self.party_food = 200
        self.party_money = 300
        self.miles_traveled = 0
        self.days_elapsed = 0
        self.weather = 'Clear'
        self.conditions = ['Clear', 'Rainy', 'Stormy', 'Snowy']
        self.event_prob = {'Weather': 20, 'Bandits': 10, 'Illness': 10}

    def display_status(self):
        print("\n----- Status -----")
        print(f"Player: {self.player_name}")
        print(f"Miles Traveled: {self.miles_traveled}")
        print(f"Days Elapsed: {self.days_elapsed}")
        print(f"Health: {self.party_health}")
        print(f"Food: {self.party_food}")
        print(f"Money: ${self.party_money}")
        print(f"Weather: {self.weather}")
        print("------------------\n")

    def travel(self):
        days = random.randint(1, 3)
        self.days_elapsed += days
        miles = random.randint(50, 100)
        self.miles_traveled += miles
        self.party_food -= random.randint(10, 20) * days
        self.party_health -= random.randint(5, 15) * days
        self.weather = random.choice(self.conditions)
        print(f"You traveled {miles} miles.")
        self.display_status()

    def rest(self):
        days = random.randint(1, 3)
        self.days_elapsed += days
        self.party_food -= random.randint(5, 10) * days
        self.party_health += random.randint(10, 20) * days
        if self.party_health > 100:
            self.party_health = 100
        self.weather = random.choice(self.conditions)
        print(f"You rested for {days} days.")
        self.display_status()

    def hunt(self):
        days = random.randint(1, 2)
        self.days_elapsed += days
        food = random.randint(50, 100)
        self.party_food += food
        self.party_health -= random.randint(5, 15) * days
        self.weather = random.choice(self.conditions)
        print(f"You hunted and found {food} pounds of food.")
        self.display_status()

    def shop(self):
        print("\nYou visit a nearby town to shop.")
        print("Food is $2 per pound.")
        print("Health recovery is $10 per 10%.")
        print("What would you like to buy?")
        print("1. Buy Food")
        print("2. Buy Health Recovery")
        print("3. Exit Shop")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            pounds = int(input("Enter pounds of food to buy: "))
            cost = pounds * 2
            if cost <= self.party_money:
                self.party_food += pounds
                self.party_money -= cost
                print(f"You bought {pounds} pounds of food.")
            else:
                print("Not enough money.")
        elif choice == '2':
            recovery = int(input("Enter percentage of health to recover (10% per $10): "))
            cost = recovery * 10
            if cost <= self.party_money:
                self.party_health += recovery
                if self.party_health > 100:
                    self.party_health = 100
                self.party_money -= cost
                print(f"You recovered {recovery}% health.")
            else:
                print("Not enough money.")
        elif choice == '3':
            print("Exiting shop.")
        else:
            print("Invalid choice.")

        self.display_status()

    def check_status(self):
        if self.party_health <= 0:
            print("\nYour party has perished. Game over!")
            return False
        elif self.miles_traveled >= 1000:
            print("\nCongratulations! You have reached your destination!")
            return False
        elif self.party_food <= 0:
            print("\nYour party has run out of food. Game over!")
            return False
        elif self.party_money <= 0:
            print("\nYou ran out of money. Game over!")
            return False
        return True

    def event(self):
        event_chance = random.randint(1, 100)
        if event_chance <= 30:
            print("\nYou encountered a random event!")
            event = random.choices(list(self.event_prob.keys()), weights=list(self.event_prob.values()))[0]
            if event == 'Weather':
                self.weather = random.choice(self.conditions)
                print(f"The weather has changed to {self.weather}!")
            elif event == 'Bandits':
                stolen_money = random.randint(10, 50)
                self.party_money -= stolen_money
                print(f"Bandits have stolen ${stolen_money}.")
            elif event == 'Illness':
                illness_health_loss = random.randint(10, 30)
                self.party_health -= illness_health_loss
                print(f"One of your party members fell ill and lost {illness_health_loss} health.")
            print("------------------")
            self.display_status()

    def play_game(self):
        print("Welcome to the Oregon Trail-like Text-Based Adventure Game!")
        print("Your goal is to travel 1000 miles with your party.")
        print("You must manage your resources wisely.")
        print("Good luck!\n")

        while self.check_status():
            print("\nWhat would you like to do next?")
            print("1. Travel")
            print("2. Rest")
            print("3. Hunt for Food")
            print("4. Visit Shop")
            print("5. Check Status")
            print("6. Exit Game")
            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                self.travel()
            elif choice == '2':
                self.rest()
            elif choice == '3':
                self.hunt()
            elif choice == '4':
                self.shop()
            elif choice == '5':
                self.display_status()
            elif choice == '6':
                print("\nExiting the game...")
                break
            else:
                print("\nInvalid choice. Please enter a number from 1 to 6.")

            self.event()
            time.sleep(1)  # Add delay for readability

if __name__ == "__main__":
    player_name = input("Enter your player's name: ").strip()
    game = OregonTrailGame(player_name)
    game.play_game()
