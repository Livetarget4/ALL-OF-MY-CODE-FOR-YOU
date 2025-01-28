import random  

class Game:  
    def __init__(self):  
        self.inventory = []  
        self.current_location = "Cave Entrance"  
        self.locations = {  
            "Cave Entrance": {  
                "description": "You stand at the mouth of a dark cave. There's a flickering light deeper inside.",  
                "options": ["Enter the cave", "Search for clues"],  
                "next": ["Inside Cave", "Clue Area"]  
            },  
            "Inside Cave": {  
                "description": "You find glowing crystals illuminating the cave. A shadow moves nearby!",  
                "options": ["Investigate shadow", "Grab a crystal"],  
                "next": ["Shadow Encounter", "Cave Exit"]  
            },  
            "Clue Area": {  
                "description": "You find ancient carvings on the walls. One of them glows faintly.",  
                "options": ["Touch the carving", "Return to the entrance"],  
                "next": ["Carving Interaction", "Cave Entrance"]  
            },  
            "Shadow Encounter": {  
                "description": "The shadow is a protector of the cave. It challenges you to answer a riddle!",  
                "options": ["Try to answer", "Run back"],  
                "next": ["Riddle", "Inside Cave"]  
            },  
            "Cave Exit": {  
                "description": "You exit the cave holding a crystal. You feel it pulsing with energy.",  
                "options": ["Return to cave", "Inspect crystal"],  
                "next": ["Inside Cave", "Inspect Crystal"]  
            },  
            "Carving Interaction": {  
                "description": "The carving reveals another path through the cave.",  
                "options": ["Go through the path", "Return to clue area"],  
                "next": ["Secret Path", "Clue Area"]  
            },  
            "Inspect Crystal": {  
                "description": "The crystal resonates. You unlock a part of the cave's history.",  
                "options": ["Return to cave", "Leave the cave"],  
                "next": ["Inside Cave", "Game Over"]  
            },  
            "Secret Path": {  
                "description": "You enter a hidden chamber filled with treasures, but beware of the curse!",  
                "options": ["Take treasure", "Leave it be"],  
                "next": ["Game Over", "Cave Exit"]  
            }  
        }  

    def play(self):  
        while True:  
            print("\n" + self.locations[self.current_location]["description"])  
            options = self.locations[self.current_location]["options"]  
            for i, option in enumerate(options, 1):  
                print(f"{i}. {option}")  

            choice = input("Choose an option (1-{}): ".format(len(options)))  
            if choice.isdigit() and 1 <= int(choice) <= len(options):  
                self.current_location = self.locations[self.current_location]["next"][int(choice) - 1]  
                if self.current_location == "Game Over":  
                    print("You have met your fate. The adventure ends here.")  
                    break  
            else:  
                print("Invalid choice, try again.")  

# Start the game  
if __name__ == '__main__':  
    game = Game()  
    game.play()  
