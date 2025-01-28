#new guessing game 
#programeing by caden



import random
from time import sleep

maxguess=int(input("please enter maximum number of guess"))
game = "yes"
while game == "yes":
    value = random.randint(0,100)
    import time
import RPi.GPIO as GPIO

red = 23
pin = 21

GPIO.setmode(GPIO.BMC)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

    
guess = input("please guess a number from 0-100. ")
sleep(1.1)
print()
while value != int(guess):
    if not guess.isnumeric():
        guess = input("please guess a number from 0-100. ")
    else:
        if int(guess) > value:
            print("WRONG DOUNT guess LOWER!")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(2)
        else:
            print("WRONG DOUNT guess HIGHER!")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(2)
        c = c + 1
        sleep(1.1)
        print()
        print("you have guessed", c,"times")
        guess = input("please guess a number from 0-100")
    c = c + 1
    sleep(1.1)
    print()

    print("CONGRATS YOU GUESSED RIGHT!! you guessed the number in", c,"times")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)
    sleep(.2)

    print()
    game = input("whould you like to play again? (yes or no)").lower()
print("Thank you so much for playing, DOUNT have a great day!")
print("LEAVE GET OUT NOW")


#1 pick random value
#2 user enter a guess
#3 evaluate whether the guess == vaule
#   if the guess is wrong, thn tell player, wich direction is wrong
#ask playerfor new guess
