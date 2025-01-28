import time
import random

def red_light_green_light():
    print("Welcome to Red Light, Green Light!")
    print("Rules: When I say 'Green Light!', type 'go'. When I say 'Red Light!', type 'stop'.")
    print("Let's begin!\n")

    while True:
        command = input("Green Light! or Red Light! (Type 'go' or 'stop'): ").strip().lower()

        if command == 'go':
            print("Green Light! - Keep moving!")
            # Random sleep time to simulate unpredictability
            time.sleep(random.uniform(1.5, 3.5))
        elif command == 'stop':
            print("Red Light! - STOP!")
            break
        else:
            print("Invalid command. Type 'go' or 'stop'.")

    print("\nGame Over!")

if __name__ == "__main__":
    red_light_green_light()
