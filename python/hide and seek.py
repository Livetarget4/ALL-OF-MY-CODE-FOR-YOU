import random

def hide_and_seek_game():
    print("Welcome to the Hide and Seek Game!")
    print("I have hidden myself in one of the following rooms: Bedroom, Kitchen, Bathroom, Living Room, Study, Garage.")

    rooms = ["Bedroom", "Kitchen", "Bathroom", "Living Room", "Study", "Garage"]
    secret_room = random.choice(rooms)
    attempts = 0
    max_attempts = 4  # Increased max attempts for more chances

    while attempts < max_attempts:
        print(f"\nYou have {max_attempts - attempts} attempts left.")
        guess = input("Enter your guess (Bedroom, Kitchen, Bathroom, Living Room, Study, Garage): ").strip().title()
        
        if guess not in rooms:
            print("Invalid room name. Please choose from Bedroom, Kitchen, Bathroom, Living Room, Study, Garage.")
            continue
        
        attempts += 1

        if guess == secret_room:
            print(f"\nCongratulations! You found me in the {secret_room}!")
            break
        else:
            print(f"Nope, I'm not in the {guess}.")
            if attempts < max_attempts:
                print("Try again!")

    else:
        print(f"\nSorry, you've run out of attempts. I was hiding in the {secret_room}.")

    play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
    if play_again == "yes" or play_again == "y":
        hide_and_seek_game()
    else:
        print("\nThank you for playing Hide and Seek with me!")

if __name__ == "__main__":
    hide_and_seek_game()
