import pygame
import random

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

# Create initial obstacles falling from the top and sides
for _ in range(num_obstacles):
    side = random.choice(["top", "left", "right"])  # Choose top, left, or right side
    if side == "top":
        obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
        obstacle_y = random.randint(-SCREEN_HEIGHT, -OBSTACLE_SIZE)
        obstacle_dx = 0  # No horizontal movement
        obstacle_dy = random.randint(1, 3)  # Random initial downward velocity
    elif side == "left":
        obstacle_x = random.randint(-OBSTACLE_SIZE, SCREEN_WIDTH // 2 - OBSTACLE_SIZE)
        obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)
        obstacle_dx = random.randint(1, 3)  # Random initial horizontal velocity towards the right
        obstacle_dy = 0  # No vertical movement
    else:  # side == "right"
        obstacle_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH)
        obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE)
        obstacle_dx = random.randint(-3, -1)  # Random initial horizontal velocity towards the left
        obstacle_dy = 0  # No vertical movement

    obstacles.append((obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, side))

# Initialize score
score = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for arrow keys
    keys = pygame.key.get_pressed()

    # Update dot position based on arrow key input
    if keys[pygame.K_LEFT]:
        dot_x -= dot_speed
    elif keys[pygame.K_RIGHT]:
        dot_x += dot_speed
    if keys[pygame.K_UP]:
        dot_y -= dot_speed
    elif keys[pygame.K_DOWN]:
        dot_y += dot_speed

    # Clear the screen
    screen.fill(BG_COLOR)

    # Update obstacles
    for i in range(num_obstacles):
        obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, side = obstacles[i]

        # Update obstacle position
        obstacle_x += obstacle_dx
        obstacle_y += obstacle_dy

        # Check collision with screen edges for obstacle
        if side == "top":
            if obstacle_y >= SCREEN_HEIGHT:  # If obstacle falls below the screen, respawn at the top
                obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
                obstacle_y = random.randint(-SCREEN_HEIGHT, -OBSTACLE_SIZE)
                obstacle_dy = random.randint(1, 3)
        elif side == "left" or side == "right":
            if obstacle_x <= 0 or obstacle_x >= SCREEN_WIDTH - OBSTACLE_SIZE:
                obstacle_dx = -obstacle_dx
            if obstacle_y <= 0 or obstacle_y >= SCREEN_HEIGHT - OBSTACLE_SIZE:
                obstacle_dy = -obstacle_dy

        # Update obstacle information in list
        obstacles[i] = (obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, side)

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
