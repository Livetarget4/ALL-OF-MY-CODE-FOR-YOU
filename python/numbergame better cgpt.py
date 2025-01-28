import random

def number_game():
    print("Welcome to the Number Guessing Game!")
    print("I have chosen a number between 1 and 100.")
    
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7  # Reduced max attempts for added challenge

    while attempts < max_attempts:
        try:
            print(f"You have {max_attempts - attempts} attempts left.")
            guess = int(input("Enter your guess (between 1 and 100): "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please enter a number within the valid range (1-100).")
                continue  # Skip the rest of the loop and restart the current iteration

            if guess < secret_number:
                print("Too low. Try again.")
            elif guess > secret_number:
                print("Too high. Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
                break
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    else:
        print(f"Sorry, you've run out of attempts. The number was {secret_number}.")

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == "yes" or play_again == "y":
        number_game()
    else:
        print("Thank you for playing!")

if __name__ == "__main__":
    number_game()
