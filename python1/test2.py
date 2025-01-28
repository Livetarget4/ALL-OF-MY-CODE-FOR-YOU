import random  


class Character:  
    def __init__(self, name):  
        self.name = name  
        self.hp = 10  # Starting hit points  
        self.attack_power = random.randint(1, 8)  # Random attack power (1d8)  
        self.defense = random.randint(1, 5)  # Random defense value (1d5)  
        self.healing_potion = 1  # Number of healing potions  

    def roll_dice(self, sides):  
        return random.randint(1, sides)  

    def attack(self, other):  
        damage = self.roll_dice(8) + self.attack_power - other.defense  # Roll 1d8 + attack power - enemy defense  
        damage = max(damage, 0)  # Prevent negative damage  
        other.hp -= damage  
        print(f"{self.name} attacks {other.name} for {damage} damage. {other.name} has {other.hp} HP left.")  

    def heal(self):  
        if self.healing_potion > 0:  
            heal_amount = self.roll_dice(6)  # Heal 1d6  
            self.hp += heal_amount  
            self.healing_potion -= 1  
            print(f"{self.name} heals for {heal_amount}. {self.name} now has {self.hp} HP.")  
        else:  
            print(f"{self.name} has no healing potions left!")  

    def is_alive(self):  
        return self.hp > 0  


def main():  
    print("Welcome to the D&D simple combat simulator!")  
    
    player_name = input("Enter your character's name: ")  
    player = Character(player_name)  
    enemy = Character("Enemy Goblin")  

    print(f"{player.name} has {player.hp} HP, {player.attack_power} attack power, and {player.defense} defense.")  
    print(f"{enemy.name} has {enemy.hp} HP, {enemy.attack_power} attack power, and {enemy.defense} defense.")  

    while player.is_alive() and enemy.is_alive():  
        print("\nChoose your action:")  
        print("1. Attack")  
        print("2. Heal (uses 1 healing potion)")  
        action = input("Enter the number of your action: ")  

        if action == "1":  
            player.attack(enemy)  
        elif action == "2":  
            player.heal()  
        else:  
            print("Invalid action. Please choose again.")  

        if enemy.is_alive():  
            enemy.attack(player)  
        else:  
            print(f"{enemy.name} has been defeated!")  

    if not player.is_alive():  
        print(f"{player.name} has been defeated. Game Over!")  


if __name__ == "__main__":  
    main()
