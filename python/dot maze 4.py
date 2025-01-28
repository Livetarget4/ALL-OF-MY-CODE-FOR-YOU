import pygame
import random

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
DOT_SIZE = 10
OBSTACLE_SIZE = 14
POWERUP_SIZE = 12
BG_COLOR = (255, 255, 255)
DOT_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
POWERUP_COLOR = (0, 255, 0)
SCORE_COLOR = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Game")

clock = pygame.time.Clock()

dot_x = SCREEN_WIDTH // 2
dot_y = SCREEN_HEIGHT // 2

# List to hold obstacle information
obstacles = []
num_obstacles = 66  # Number of obstacles
# Create initial obstacles with random positions and velocities
for _ in range(num_obstacles):
    obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
    obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)
    obstacle_dx = random.randint(-2, 2)  # Random initial velocity in x direction
    obstacle_dy = random.randint(-2, 2)  # Random initial velocity in y direction
    obstacles.append((obstacle_x, obstacle_y, obstacle_dx, obstacle_dy))

# List to hold power-up information
powerups = []
num_powerups = 5  # Number of power-ups
# Create initial power-ups with random positions
for _ in range(num_powerups):
    powerup_x = random.randint(0, SCREEN_WIDTH - POWERUP_SIZE)
    powerup_y = random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE)
    powerups.append((powerup_x, powerup_y))

# Initialize score
score = 0

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
        if (dot_x + DOT_SIZE >= obstacle_x and dot_x <= obstacle_x + OBSTACLE_SIZE and
            dot_y + DOT_SIZE >= obstacle_y and dot_y <= obstacle_y + OBSTACLE_SIZE):
            running = False

    # Update power-ups
    for i in range(num_powerups):
        powerup_x, powerup_y = powerups[i]

        # Draw the power-up
        pygame.draw.rect(screen, POWERUP_COLOR, (powerup_x, powerup_y, POWERUP_SIZE, POWERUP_SIZE))

        # Check collision between dot and power-up
        if (dot_x + DOT_SIZE >= powerup_x and dot_x <= powerup_x + POWERUP_SIZE and
            dot_y + DOT_SIZE >= powerup_y and dot_y <= powerup_y + POWERUP_SIZE):
            # Apply power-up effect (temporary speed boost)
            dot_speed_boost = 2
            pygame.time.set_timer(pygame.USEREVENT+1, 5000)  # Set timer for 5 seconds
            # Remove the power-up from the list
            powerups[i] = (-100, -100)  # Move power-up off-screen

    # Get mouse position (to control the dot)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the dot towards the mouse cursor
    if dot_x < mouse_x:
        dot_x += dot_speed_boost  # Apply speed boost if active
    elif dot_x > mouse_x:
        dot_x -= dot_speed_boost
    if dot_y < mouse_y:
        dot_y += dot_speed_boost
    elif dot_y > mouse_y:
        dot_y -= dot_speed_boost

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
