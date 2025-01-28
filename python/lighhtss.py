import time
import RPi.GPIO as GPIO

red = 23
pin = 21

GPIO.setmode(GPIO.BMC)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

x=int(input("how long do you whant light on"))
y=int(input("how long do you between lights?"))

while True:
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pin (GPIO.LOW)
    time.sleep(2)

    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pin (GPIO.LOW)
    time.sleep(2) 
