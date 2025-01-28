import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
DOT_SIZE = 10
OBSTACLE_SIZE = 20
BG_COLOR = (255, 255, 255)
DOT_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Game")

clock = pygame.time.Clock()

dot_x = SCREEN_WIDTH // 2
dot_y = SCREEN_HEIGHT // 2


obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)
obstacle_dx = random.choice([-1, 1])  # Random initial direction
obstacle_dy = random.choice([-1, 1])  # Random initial direction

obstacle_a = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
obstacle_b = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)
obstacle_da = random.choice([-2, 2])  # Random initial direction
obstacle_db = random.choice([-2, 2])  # Random initial direction

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Update obstacle position
    obstacle_x += obstacle_dx
    obstacle_y += obstacle_dy
    obstacle_a += obstacle_da
    obstacle_b += obstacle_db

    # Check collision with screen edges for obstacle
    if obstacle_x <= 0 or obstacle_x >= SCREEN_WIDTH - OBSTACLE_SIZE:
        obstacle_dx = -obstacle_dx
    if obstacle_y <= 0 or obstacle_y >= SCREEN_HEIGHT - OBSTACLE_SIZE:
        obstacle_dy = -obstacle_dy
    if obstacle_a <= 0 or obstacle_a >= SCREEN_WIDTH - OBSTACLE_SIZE:
        obstacle_da = -obstacle_da
    if obstacle_b <= 0 or obstacle_b >= SCREEN_WIDTH - OBSTACLE_SIZE:
        obstacle_db = -obstacle_db

    # Draw the obstacle
    pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))

    # Get mouse position (to control the dot)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the dot towards the mouse cursor
    if dot_x < mouse_x:
        dot_x += 1
    elif dot_x > mouse_x:
        dot_x -= 1
    if dot_y < mouse_y:
        dot_y += 1
    elif dot_y > mouse_y:
        dot_y -= 1

    # Draw the dot (player)
    pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), DOT_SIZE)

    # Check collision between dot and obstacle
    if (dot_x + DOT_SIZE >= obstacle_x and dot_x <= obstacle_x + OBSTACLE_SIZE and
        dot_y + DOT_SIZE >= obstacle_y and dot_y <= obstacle_y + OBSTACLE_SIZE):
        running = False

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
