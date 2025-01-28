import random
import time
import json
import os
from typing import Dict, List, Tuple

class AdventureGame:
    def __init__(self):
        self.player = {
            "name": "",
            "class": "",
            "level": 1,
            "xp": 0,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "gold": 100,
            "inventory": {},
            "equipment": {
                "weapon": None,
                "armor": None,
                "accessory": None
            },
            "skills": []
        }
        
        self.classes = {
            "warrior": {
                "base_hp": 120,
                "base_mp": 30,
                "skills": ["slash", "defend"]
            },
            "mage": {
                "base_hp": 80,
                "base_mp": 100,
                "skills": ["fireball", "heal"]
            },
            "ranger": {
                "base_hp": 90,
                "base_mp": 60,
                "skills": ["quick_shot", "trap"]
            }
        }
        
        self.items = {
            "health_potion": {"type": "consumable", "effect": "heal", "value": 50, "price": 50},
            "mana_potion": {"type": "consumable", "effect": "mana", "value": 30, "price": 40},
            "wooden_sword": {"type": "weapon", "attack": 5, "price": 100},
            "iron_sword": {"type": "weapon", "attack": 10, "price": 200},
            "leather_armor": {"type": "armor", "defense": 5, "price": 150},
            "iron_armor": {"type": "armor", "defense": 10, "price": 300},
            "lucky_charm": {"type": "accessory", "effect": "luck", "value": 5, "price": 250}
        }
        
        self.enemies = {
            "slime": {"hp": 30, "attack": 5, "xp": 10, "gold": (5, 15)},
            "goblin": {"hp": 45, "attack": 8, "xp": 15, "gold": (10, 25)},
            "wolf": {"hp": 60, "attack": 12, "xp": 20, "gold": (15, 35)},
            "orc": {"hp": 100, "attack": 15, "xp": 30, "gold": (25, 50)},
            "dragon": {"hp": 200, "attack": 25, "xp": 100, "gold": (100, 200)}
        }
        
        self.locations = {
            "town": ["shop", "inn", "quest_board"],
            "forest": ["slime", "goblin", "wolf"],
            "cave": ["goblin", "wolf", "orc"],
            "mountain": ["wolf", "orc", "dragon"]
        }
        
        self.current_location = "town"
        self.quests = []
        self.generate_quests()

    def generate_quests(self):
        quest_types = [
            ("Kill 5 slimes", "slime", 5, 100),
            ("Defeat 3 goblins", "goblin", 3, 150),
            ("Hunt 2 wolves", "wolf", 2, 200),
            ("Slay 1 orc", "orc", 1, 300)
        ]
        self.quests = [
            {
                "description": desc,
                "target": target,
                "amount": amount,
                "reward": reward,
                "progress": 0,
                "completed": False
            }
            for desc, target, amount, reward in quest_types
        ]

    def create_character(self):
        print("\n=== Character Creation ===")
        self.player["name"] = input("Enter your character's name: ")
        
        print("\nAvailable Classes:")
        for class_name in self.classes.keys():
            print(f"- {class_name.capitalize()}")
        
        while True:
            chosen_class = input("\nChoose your class: ").lower()
            if chosen_class in self.classes:
                self.player["class"] = chosen_class
                self.player["hp"] = self.classes[chosen_class]["base_hp"]
                self.player["max_hp"] = self.classes[chosen_class]["base_hp"]
                self.player["mp"] = self.classes[chosen_class]["base_mp"]
                self.player["max_mp"] = self.classes[chosen_class]["base_mp"]
                self.player["skills"] = self.classes[chosen_class]["skills"]
                break
            print("Invalid class choice!")

    def display_status(self):
        print(f"\n=== {self.player['name']} the {self.player['class'].capitalize()} ===")
        print(f"Level: {self.player['level']} (XP: {self.player['xp']})")
        print(f"HP: {self.player['hp']}/{self.player['max_hp']}")
        print(f"MP: {self.player['mp']}/{self.player['max_mp']}")
        print(f"Gold: {self.player['gold']}")
        
        print("\nEquipment:")
        for slot, item in self.player["equipment"].items():
            print(f"{slot.capitalize()}: {item if item else 'None'}")
        
        print("\nInventory:")
        for item, amount in self.player["inventory"].items():
            print(f"{item}: {amount}")

    def shop(self):
        print("\n=== Shop ===")
        print("Available Items:")
        for item_name, item_data in self.items.items():
            print(f"{item_name}: {item_data['price']} gold")
        
        while True:
            choice = input("\nWhat would you like to buy? (or 'exit' to leave): ").lower()
            if choice == "exit":
                break
            
            if choice in self.items:
                if self.player["gold"] >= self.items[choice]["price"]:
                    self.player["gold"] -= self.items[choice]["price"]
                    self.player["inventory"][choice] = self.player["inventory"].get(choice, 0) + 1
                    print(f"Bought {choice}!")
                else:
                    print("Not enough gold!")
            else:
                print("Invalid item!")

    def use_item(self):
        if not self.player["inventory"]:
            print("No items in inventory!")
            return
        
        print("\n=== Inventory ===")
        for item, amount in self.player["inventory"].items():
            print(f"{item}: {amount}")
        
        choice = input("\nWhat would you like to use? ").lower()
        if choice in self.player["inventory"] and self.player["inventory"][choice] > 0:
            item_data = self.items[choice]
            if item_data["type"] == "consumable":
                if item_data["effect"] == "heal":
                    self.player["hp"] = min(self.player["hp"] + item_data["value"], self.player["max_hp"])
                    print(f"Restored {item_data['value']} HP!")
                elif item_data["effect"] == "mana":
                    self.player["mp"] = min(self.player["mp"] + item_data["value"], self.player["max_mp"])
                    print(f"Restored {item_data['value']} MP!")
                self.player["inventory"][choice] -= 1
            elif item_data["type"] in ["weapon", "armor", "accessory"]:
                self.equip_item(choice, item_data)
        else:
            print("Invalid item!")

    def equip_item(self, item_name: str, item_data: Dict):
        slot = item_data["type"]
        if self.player["equipment"][slot]:
            self.player["inventory"][self.player["equipment"][slot]] = self.player["inventory"].get(self.player["equipment"][slot], 0) + 1
        
        self.player["equipment"][slot] = item_name
        self.player["inventory"][item_name] -= 1
        print(f"Equipped {item_name}!")

    def combat(self, enemy_type: str):
        enemy = self.enemies[enemy_type].copy()
        print(f"\nA {enemy_type} appears!")
        
        while enemy["hp"] > 0 and self.player["hp"] > 0:
            print(f"\nYour HP: {self.player['hp']}/{self.player['max_hp']}")
            print(f"Enemy HP: {enemy['hp']}")
            print("\nActions:")
            print("1. Attack")
            print("2. Use Skill")
            print("3. Use Item")
            print("4. Run")
            
            choice = input("Choose your action: ")
            
            if choice == "1":
                damage = 10  # Base damage
                if self.player["equipment"]["weapon"]:
                    damage += self.items[self.player["equipment"]["weapon"]]["attack"]
                enemy["hp"] -= damage
                print(f"You deal {damage} damage!")
                
            elif choice == "2":
                self.use_skill(enemy)
                
            elif choice == "3":
                self.use_item()
                continue
                
            elif choice == "4":
                if random.random() < 0.5:
                    print("Got away safely!")
                    return
                print("Couldn't escape!")
            
            if enemy["hp"] > 0:
                damage = enemy["attack"]
                if self.player["equipment"]["armor"]:
                    damage = max(1, damage - self.items[self.player["equipment"]["armor"]]["defense"])
                self.player["hp"] -= damage
                print(f"Enemy deals {damage} damage!")
        
        if self.player["hp"] > 0:
            gold_reward = random.randint(*enemy["gold"])
            self.player["gold"] += gold_reward
            self.player["xp"] += enemy["xp"]
            print(f"\nVictory! Gained {enemy['xp']} XP and {gold_reward} gold!")
            
            # Update quest progress
            for quest in self.quests:
                if not quest["completed"] and quest["target"] == enemy_type:
                    quest["progress"] += 1
                    if quest["progress"] >= quest["amount"]:
                        quest["completed"] = True
                        self.player["gold"] += quest["reward"]
                        print(f"\nQuest completed! Received {quest['reward']} gold!")
            
            self.check_level_up()
        else:
            print("\nGame Over!")

    def use_skill(self, enemy: Dict):
        if not self.player["skills"]:
            print("No skills available!")
            return
        
        print("\nAvailable Skills:")
        for i, skill in enumerate(self.player["skills"], 1):
            print(f"{i}. {skill}")
        
        try:
            choice = int(input("Choose a skill: ")) - 1
            if 0 <= choice < len(self.player["skills"]):
                skill = self.player["skills"][choice]
                if self.player["mp"] >= 10:
                    self.player["mp"] -= 10
                    if skill == "fireball":
                        damage = 20
                        enemy["hp"] -= damage
                        print(f"Fireball deals {damage} damage!")
                    elif skill == "heal":
                        heal = 30
                        self.player["hp"] = min(self.player["hp"] + heal, self.player["max_hp"])
                        print(f"Healed for {heal} HP!")
                    elif skill == "slash":
                        damage = 15
                        enemy["hp"] -= damage
                        print(f"Slash deals {damage} damage!")
                    elif skill == "quick_shot":
                        damage = 12
                        enemy["hp"] -= damage
                        print(f"Quick Shot deals {damage} damage!")
                else:
                    print("Not enough MP!")
            else:
                print("Invalid skill choice!")
        except ValueError:
            print("Invalid input!")

    def check_level_up(self):
        xp_needed = self.player["level"] * 100
        if self.player["xp"] >= xp_needed:
            self.player["level"] += 1
            self.player["xp"] -= xp_needed
            self.player["max_hp"] += 10
            self.player["max_mp"] += 5
            self.player["hp"] = self.player["max_hp"]
            self.player["mp"] = self.player["max_mp"]
            print(f"\nLevel Up! You are now level {self.player['level']}!")

    def rest_at_inn(self):
        cost = 20
        if self.player["gold"] >= cost:
            self.player["gold"] -= cost
            self.player["hp"] = self.player["max_hp"]
            self.player["mp"] = self.player["max_mp"]
            print(f"Rested at the inn. HP and MP fully restored! (-{cost} gold)")
        else:
            print("Not enough gold to rest at the inn!")

    def view_quests(self):
        print("\n=== Quest Board ===")
        for i, quest in enumerate(self.quests, 1):
            status = "Completed" if quest["completed"] else f"Progress: {quest['progress']}/{quest['amount']}"
            print(f"{i}. {quest['description']} - {status}")
            if not quest["completed"]:
                print(f"   Reward: {quest['reward']} gold")

    def play(self):
        self.create_character()
        
        while True:
            self.display_status()
            print(f"\nLocation: {self.current_location.capitalize()}")
            print("\nActions:")
            
            if self.current_location == "town":
                print("1. Go to Shop")
                print("2. Rest at Inn")
                print("3. View Quest Board")
                print("4. Go to Forest")
                print("5. Go to Cave")
                print("6. Go to Mountain")
                print("7. Use Item")
                print("8. Save Game")
                print("9. Quit")
                
                choice = input("\nChoose an action: ")
                
                if choice == "1":
                    self.shop()
                elif choice == "2":
                    self.rest_at_inn()
                elif choice == "3":
                    self.view_quests()
                elif choice == "4":
                    self.current_location = "forest"
                elif choice == "5":
                    self.current_location = "cave"
                elif choice == "6":
                    self.current_location = "mountain"
                elif choice == "7":
                    self.use_item()
                elif choice == "8":
                    self.save_game()
                elif choice == "9":
                    break
            else:
                print("1. Look for Enemies")
                print("2. Return to Town")
                print("3. Use Item")
                
                choice = input("\nChoose an action: ")
                
                if choice == "1":
                    enemy = random.choice(self.locations[self.current_location])
                    self.combat(enemy)
                    if self.player["hp"] <= 0:
                        break
                elif choice == "2":
                    self.current_location = "town"
                elif choice == "3":
                    self.use_item()

    def save_game(self):
        game_state = {
            "player": self.player,
            "current_location": self.current_location,
            "quests": self.quests
        }
        try:
            # Print the data being saved (for debugging)
            print("Attempting to save:", game_state)
            
            # Use proper JSON formatting with indentation
            with open("savegame.json", "w", encoding='utf-8') as f:
                json.dump(game_state, f, indent=4, default=str)
            
            # Verify the file was created
            if not os.path.exists("savegame.json"):
                raise Exception("File was not created")
                
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {str(e)}")

    def load_game(self):
        try:
            # Check if file exists before attempting to load
            if not os.path.exists("savegame.json"):
                print("No save file found.")
                return False
            
            # Print the contents of the file (for debugging)
            with open("savegame.json", "r", encoding='utf-8') as f:
                print("Reading file contents:", f.read())
                f.seek(0)  # Reset file pointer to beginning
                game_state = json.load(f)
            
            # Validate the loaded data has required keys
            required_keys = ["player", "current_location", "quests"]
            if not all(key in game_state for key in required_keys):
                raise KeyError("Save file is missing required data")
            
            self.player = game_state["player"]
            self.current_location = game_state["current_location"]
            self.quests = game_state["quests"]
            
            print("Game loaded successfully!")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error decoding save file: {str(e)}")
            return False
        except Exception as e:
            print(f"Error loading game: {str(e)}")
            return False

if __name__ == "__main__":
    game = AdventureGame()
    
    print("=== Welcome to the Adventure Game ===")
    print("1. New Game")
    print("2. Load Game")
    
    choice = input("Choose an option: ")
    
    if choice == "2" and game.load_game():
        game.play()
    else:
        game.play()
