from time import sleep
import RPi.GPIO as GPIO

red = 23
green = 21
yellow = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)

while True:
    GPIO.output(red, GPIO.HIGH)
    sleep(1.5)
    GPIO.output(red, GPIO.LOW)

    GPIO.output(green, GPIO.HIGH)
    sleep(1.5)
    GPIO.output(green, GPIO.LOW)

    GPIO.output(yellow, GPIO.HIGH)
    sleep(1.5)
    GPIO.output(yellow, GPIO.LOW)
