import pygame
import random

pygame.init()


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
DOT_SIZE = 10
OBSTACLE_SIZE = 14
BG_COLOR = (255, 255, 255)
DOT_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Game")

clock = pygame.time.Clock()

dot_x = SCREEN_WIDTH // 2
dot_y = SCREEN_HEIGHT // 2

#!/usr/bin/env python3

import time
import smbus

BUS = smbus.SMBus(1)

def write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr ,temp)

def send_command(comm):
	# Send bit7-4 firstly
	buf = comm & 0xF0
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (comm & 0x0F) << 4
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def send_data(data):
	# Send bit7-4 firstly
	buf = data & 0xF0
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (data & 0x0F) << 4
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def init(addr, bl):
#	global BUS
#	BUS = smbus.SMBus(1)
	global LCD_ADDR
	global BLEN
	LCD_ADDR = addr
	BLEN = bl
	try:
		send_command(0x33) # Must initialize to 8-line mode at first
		time.sleep(0.005)
		send_command(0x32) # Then initialize to 4-line mode
		time.sleep(0.005)
		send_command(0x28) # 2 Lines & 5*7 dots
		time.sleep(0.005)
		send_command(0x0C) # Enable display without cursor
		time.sleep(0.005)
		send_command(0x01) # Clear Screen
		BUS.write_byte(LCD_ADDR, 0x08)
	except:
		return False
	else:
		return True

def clear():
	send_command(0x01) # Clear Screen

def openlight():  # Enable the backlight
	BUS.write_byte(0x27,0x08)
	BUS.close()

def write(x, y, str):
	if x < 0:
		x = 0
	if x > 15:
		x = 15
	if y <0:
		y = 0
	if y > 1:
		y = 1

	# Move cursor
	addr = 0x80 + 0x40 * y + x
	send_command(addr)

	for chr in str:
		send_data(ord(chr))


# List to hold obstacle information
obstacles = []
num_obstacles = 66  # Number of obstacles
username = input("what is your name? ")
# Create initial obstacles with random positions and velocities
for _ in range(num_obstacles):
    obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
    obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)

    if (SCREEN_WIDTH / 2 - 200 < obstacle_x < SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 2 - 200 < obstacle_y < SCREEN_HEIGHT / 2 + 200 ):
        obstacle_x += 200
    
    obstacle_dx = random.randint(-2, 2)  # Random initial velocity in x direction
    obstacle_dy = random.randint(-2, 2)  # Random initial velocity in y direction
    obstacles.append((obstacle_x, obstacle_y, obstacle_dx, obstacle_dy))
    start = time.time()#'''THIS IS FOR START DISPLAY'''

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Update obstacles
    for i in range(num_obstacles):
        obstacle_x, obstacle_y, obstacle_dx, obstacle_dy = obstacles[i]

        # Update obstacle position
        obstacle_x += obstacle_dx
        obstacle_y += obstacle_dy

        # Check collision with screen edges for obstacle
        if obstacle_x <= 0 or obstacle_x >= SCREEN_WIDTH - OBSTACLE_SIZE:
            obstacle_dx = -obstacle_dx
        if obstacle_y <= 0 or obstacle_y >= SCREEN_HEIGHT - OBSTACLE_SIZE:
            obstacle_dy = -obstacle_dy

        # Update obstacle information in list
        obstacles[i] = (obstacle_x, obstacle_y, obstacle_dx, obstacle_dy)

        # Draw the obstacle
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))

        # Check collision between dot and obstacle
        if True:
            if (dot_x + DOT_SIZE >= obstacle_x and dot_x <= obstacle_x + OBSTACLE_SIZE and
                dot_y + DOT_SIZE >= obstacle_y and dot_y <= obstacle_y + OBSTACLE_SIZE):
                end = time.time()
                score = round(end - start)
                init(0x27, 1)
                write(0, 0,  username+ ' Score') #THIS SPACE IS TO DISPLAY ENDING SCREEN
                write(0, 1, str(score))
                running = False
         

    # Get mouse position (to control the dot)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the dot towards the mouse cursor
    if dot_x < mouse_x:
        dot_x += 4
    elif dot_x > mouse_x:
        dot_x -= 4
    if dot_y < mouse_y:
        dot_y += 4
    elif dot_y > mouse_y:
        dot_y -= 4
    # Draw the dot (player)
    pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), DOT_SIZE)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
