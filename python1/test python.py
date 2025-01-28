import random

def number_guessing_game():
    number = random.randint(1, 100)
    attempts = 0

    print("Welcome to the Number Guessing Game!")

    while True:
        try:
            guess = int(input("Guess a number between 1 and 100: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess < 1 or guess > 100:
            print("Please enter a number between 1 and 100.")
            continue

        attempts += 1

        if guess < number:
            print("Too low, try again.")
        elif guess > number:
            print("Too high, try again.")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            play_again = input("Do you want to play again? (yes/no): ")

            if play_again.lower() != 'yes':
                print("Thanks for playing!")
                break
            else:
                number = random.randint(1, 100)
                attempts = 0

number_guessing_game()
