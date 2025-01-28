import PCF8591 as ADC  # Import ADC module for joystick
import time

ADC.setup(0x48)  # Setup PCF8591 ADC

def read_joystick():
    while True:
        x = ADC.read(0)
        y = ADC.read(1)
        button = ADC.read(2)
        print(f"X: {x}, Y: {y}, Button: {button}")
        time.sleep(0.1)

if __name__ == '__main__':
    read_joystick()
import pygame
import random
import PCF8591 as ADC  # Import ADC module for joystick

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 850
DOT_SIZE = 10
OBSTACLE_SIZE = 15  # Increase obstacle size for better visibility
BG_COLOR = (255, 255, 255)
DOT_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
SCORE_COLOR = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Game")

clock = pygame.time.Clock()

dot_x = SCREEN_WIDTH // 2
dot_y = SCREEN_HEIGHT // 2
dot_speed = 4  # Movement speed of the dot

# List to hold obstacle information
obstacles = []
num_obstacles = 66  # Number of obstacles
# Create initial obstacles falling from the top
for _ in range(num_obstacles):
    obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
    obstacle_y = random.randint(-SCREEN_HEIGHT, -OBSTACLE_SIZE)  # Start above the visible screen
    obstacle_dx = 0  # No horizontal movement
    obstacle_dy = random.randint(1, 3)   # Random initial downward velocity
    obstacles.append((obstacle_x, obstacle_y, obstacle_dx, obstacle_dy))

# Initialize score
score = 0

# Setup ADC module
ADC.setup(0x48)  # Setup PCF8591 ADC

# Function to get joystick direction
def direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    i = 0
    if ADC.read(0) <= 90:
        i = 1  # up
    elif ADC.read(0) >= 225:
        i = 2  # down

    if ADC.read(1) >= 225:
        i = 3  # left
    elif ADC.read(1) <= 90:
        i = 4  # right

    if ADC.read(2) <= 30:
        i = 5  # Button pressed

    if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15 and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
        i = 0

    return state[i]

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Get joystick input
    joystick_direction = direction()

    # Update dot position based on joystick input
    if joystick_direction == 'left':
        dot_x -= dot_speed
    elif joystick_direction == 'right':
        dot_x += dot_speed
    if joystick_direction == 'up':
        dot_y -= dot_speed
    elif joystick_direction == 'down':
        dot_y += dot_speed

    # Ensure dot stays within screen bounds
    if dot_x < 0:
        dot_x = 0
    elif dot_x > SCREEN_WIDTH - DOT_SIZE:
        dot_x = SCREEN_WIDTH - DOT_SIZE
    if dot_y < 0:
        dot_y = 0
    elif dot_y > SCREEN_HEIGHT - DOT_SIZE:
        dot_y = SCREEN_HEIGHT - DOT_SIZE

    # Update obstacles
    for i in range(num_obstacles):
        obstacle_x, obstacle_y, obstacle_dx, obstacle_dy = obstacles[i]

        # Update obstacle position
        obstacle_x += obstacle_dx
        obstacle_y += obstacle_dy

        # Check collision with screen edges for obstacle
        if obstacle_x <= 0 or obstacle_x >= SCREEN_WIDTH - OBSTACLE_SIZE:
            obstacle_dx = -obstacle_dx
        if obstacle_y >= SCREEN_HEIGHT:  # If obstacle falls below the screen, respawn at the top
            obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
            obstacle_y = random.randint(-SCREEN_HEIGHT, -OBSTACLE_SIZE)
            obstacle_dy = random.randint(1, 3)

        # Update obstacle information in list
        obstacles[i] = (obstacle_x, obstacle_y, obstacle_dx, obstacle_dy)

        # Draw the obstacle with increased size for better visibility
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))

        # Check collision between dot and obstacle
        if (dot_x + DOT_SIZE >= obstacle_x and dot_x <= obstacle_x + OBSTACLE_SIZE and
            dot_y + DOT_SIZE >= obstacle_y and dot_y <= obstacle_y + OBSTACLE_SIZE):
            running = False

    # Draw the dot (player)
    pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), DOT_SIZE)

    # Update and display score
    score += 1  # Increment score (you can adjust scoring logic as per your game rules)
    score_text = f"Score: {score}"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(score_text, True, SCORE_COLOR)
    screen.blit(text_surface, (10, 10))  # Display score at (10, 10) on the screen

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
