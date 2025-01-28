import pygame
import random
import PCF8591 as ADC  # Assuming PCF8591.py is your ADC library

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)  # Example of a light blue color

# Player attributes
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = WHITE
PLAYER_SPEED = 7

# Obstacle attributes
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_COLOR = BLACK
OBSTACLE_SPEED = 7  # Increased obstacle speed
OBSTACLE_INTERVAL = 750  # Interval between new obstacles in milliseconds, reduced for more frequent obstacles

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.last_obstacle_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def update_player(self, joystick_state):
        # Update player position based on joystick input
        if joystick_state == 'left':
            self.player_x -= PLAYER_SPEED
        elif joystick_state == 'right':
            self.player_x += PLAYER_SPEED

        # Boundary checking for player
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.player_x = SCREEN_WIDTH - PLAYER_WIDTH

    def update_obstacles(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > OBSTACLE_INTERVAL:
            obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            obstacle_y = -OBSTACLE_HEIGHT
            self.obstacles.append((obstacle_x, obstacle_y))
            self.last_obstacle_time = current_time

        # Update obstacle positions and handle collisions
        for i in range(len(self.obstacles) - 1, -1, -1):
            obstacle_x, obstacle_y = self.obstacles[i]
            obstacle_y += OBSTACLE_SPEED
            self.obstacles[i] = (obstacle_x, obstacle_y)

            # Check collision with player
            if (self.player_x < obstacle_x + OBSTACLE_WIDTH and
                self.player_x + PLAYER_WIDTH > obstacle_x and
                self.player_y < obstacle_y + OBSTACLE_HEIGHT and
                self.player_y + PLAYER_HEIGHT > obstacle_y):
                self.game_over = True

            # Remove obstacles that have passed the screen or collided with the player
            if obstacle_y > SCREEN_HEIGHT or self.game_over:
                self.obstacles.pop(i)
                if not self.game_over:
                    self.score += 1

    def draw_player(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def draw_obstacles(self):
        for obstacle_x, obstacle_y in self.obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def run(self):
        while not self.game_over:
            self.handle_events()

            # Get joystick state
            joystick_state = direction()

            # Clear the screen with the chosen background color
            screen.fill(LIGHT_BLUE)

            # Update player position
            self.update_player(joystick_state)

            # Update obstacles and check collisions
            self.update_obstacles()

            # Draw players
            self.draw_player()

            # Draw obstacles
            self.draw_obstacles()

            # Draw score
            self.draw_score()

            # Update screen
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()

def setup():
    ADC.setup(0x48)  # Setup PCF8591

def direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    i = 0

    if ADC.read(1) >= 225:
        i = 3  # left
    elif ADC.read(1) <= 90:
        i = 4  # right

    return state[i]

if __name__ == "__main__":
    setup()  # Initialize ADC setup
    game = Game()
    game.run()
