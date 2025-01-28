import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        
        print("Now place your tag to write")
        txt = reader.read()
        print(txt)
finally:
        GPIO.cleanup()
        
text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
