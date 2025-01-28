import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.location = "Entrance"

    def show_status(self):
        inventory_items = ", ".join(self.inventory) if self.inventory else "Empty"
        health_status = f"Health: {self.health}"
        return f"\n--- {self.name}'s Status ---\n{health_status}\nInventory: {inventory_items}\n"

class DungeonGame:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.locations = {
            "Entrance": {
                "description": "The dimly lit dungeon entrance, where the air feels damp and foreboding.",
                "connections": ["Hallway"],
                "event": "Nothing happens... for now."
            },
            "Hallway": {
                "description": "A long, narrow corridor lined with ancient, moss-covered stone.",
                "connections": ["Entrance", "Trap Room", "Treasure Room"],
                "event": random.choice([
                    "You found a shiny gold coin!",
                    "You hear whispers echoing through the hall.",
                    "A sudden gust of wind extinguishes your torch."
                ])
            },
            "Trap Room": {
                "description": "A treacherous chamber filled with loose stones and hidden dangers.",
                "connections": ["Hallway"],
                "event": random.choice([
                    "A trap springs! You narrowly avoid sharp spikes.",
                    "You step on a pressure plate and dodge flying darts.",
                    "You find a healing potion hidden among the rubble!"
                ])
            },
            "Treasure Room": {
                "description": "A glittering chamber filled with chests, gems, and ominous statues.",
                "connections": ["Hallway", "Exit"],
                "event": random.choice([
                    "You find the Dungeon Key among the treasure!",
                    "An enemy appears! Prepare for battle!",
                    "You accidentally trigger a trap, losing health."
                ])
            },
            "Exit": {
                "description": "A heavy stone door that leads to freedom.",
                "connections": [],
                "event": "The exit is within reach."
            }
        }
        self.key_found = False

    def move_player(self, destination):
        if destination in self.locations[self.player.location]["connections"]:
            self.player.location = destination
            return f"You move to the {destination}. {self.locations[destination]['description']}"
        return "You can't go there from here."

    def trigger_event(self):
        event = self.locations[self.player.location]["event"]
        if "trap" in event.lower():
            damage = random.randint(10, 30)
            self.player.health -= damage
            return f"{event} You lost {damage} health!"
        elif "healing potion" in event.lower():
            self.player.inventory.append("Healing Potion")
            return event
        elif "dungeon key" in event.lower():
            if not self.key_found:
                self.key_found = True
                self.player.inventory.append("Dungeon Key")
                return event
        elif "enemy appears" in event.lower():
            damage = random.randint(15, 35)
            self.player.health -= damage
            return f"An enemy attacks you, causing {damage} damage! You defeat it and survive."
        return event

    def use_item(self, item_name):
        if item_name in self.player.inventory:
            if item_name == "Healing Potion":
                self.player.health = min(100, self.player.health + 25)
                self.player.inventory.remove("Healing Potion")
                return "You used a Healing Potion and restored 25 health!"
            return "You can't use that item right now."
        return "You don't have that item."

    def check_exit(self):
        if self.player.location == "Exit":
            if "Dungeon Key" in self.player.inventory:
                return "You unlock the heavy door with the Dungeon Key and escape! Victory!"
            return "The door is locked. You need the Dungeon Key to open it."
        return ""

    def play(self):
        print(f"Welcome, {self.player.name}, to 'Escape the Dungeon'!")
        print("Your goal: Find the Dungeon Key and escape through the Exit.\n")
        print(self.locations[self.player.location]["description"])

        while self.player.health > 0:
            print(self.player.show_status())
            print(f"You are in the {self.player.location}.")
            print(f"Connected locations: {', '.join(self.locations[self.player.location]['connections'])}")
            action = input("\nWhat will you do? (move <location> / event / use <item> / help / exit): ").strip().lower()

            if action.startswith("move "):
                destination = action.split("move ")[1].capitalize()
                print(self.move_player(destination))
                if self.player.location == "Exit":
                    print(self.check_exit())
                    if "Dungeon Key" in self.player.inventory:
                        break
            elif action == "event":
                print(self.trigger_event())
                if self.player.health <= 0:
                    print("You succumbed to your injuries. Game over!")
                    break
            elif action.startswith("use "):
                item_name = action.split("use ")[1].capitalize()
                print(self.use_item(item_name))
            elif action == "help":
                print("\nCommands:\n"
                      "- move <location>: Move to a connected location.\n"
                      "- event: Trigger a random event in the current location.\n"
                      "- use <item>: Use an item from your inventory.\n"
                      "- help: Show available commands.\n"
                      "- exit: Quit the game.")
            elif action == "exit":
                print("Thanks for playing! Goodbye!")
                break
            else:
                print("Invalid command. Type 'help' for a list of commands.")

        if self.player.health <= 0:
            print("You have died. Better luck next time!")

if __name__ == "__main__":
    player_name = input("Enter your character's name: ").strip()
    game = DungeonGame(player_name)
    game.play()
