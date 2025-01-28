import turtle
import random
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Red Light, Green Light Game")
screen.bgcolor("white")

# Create the player (dot)
player = turtle.Turtle()
player.shape("circle")
player.color("red")
player.penup()
player.speed(0)
player.goto(-200, 0)  # Start position

# Create the traffic light
light = turtle.Turtle()
light.shape("square")
light.color("black")
light.penup()
light.speed(0)
light.goto(0, 150)
light.shapesize(3, 1)  # Larger size for visibility

# Game state variables
game_over = False
light_color = "green"

# Function to change the light color
def change_light():
    global light_color
    if light_color == "green":
        light_color = "red"
        light.color("red")
    else:
        light_color = "green"
        light.color("green")
    screen.ontimer(change_light, random.randint(3000, 6000))  # Change light randomly between 3 to 6 seconds

# Function to move the player forward
def move():
    if not game_over:
        player.forward(10)
        # Check if player reaches the traffic light
        if player.distance(light) < 20 and light_color == "red":
            player.color("red")
            player.write("Game Over!", align="center", font=("Arial", 24, "normal"))
            time.sleep(2)
            screen.bye()  # Close the window
        else:
            screen.ontimer(move, 100)

# Start the game
change_light()
move()

# Keyboard bindings
def go():
    if not game_over and light_color == "green":
        player.color("blue")
        move()

def stop():
    global game_over
    game_over = True

screen.listen()
screen.onkey(go, "g")  # "g" key for go
screen.onkey(stop, "s")  # "s" key for stop

turtle.done()
