import random

def number_game():
    print("Welcome to the Number Guessing Game!")
    print("I have chosen a number between 1 and 100.")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < secret_number:
                print("Too low. Try again.")
            elif guess > secret_number:
                print("Too high. Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
                break

            if attempts == max_attempts:
                print(f"Sorry, you've reached the maximum number of attempts. The number was {secret_number}.")
                break

        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    number_game()
