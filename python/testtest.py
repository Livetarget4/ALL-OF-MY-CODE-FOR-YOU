import pygame
import random

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
        self.player1_x = 3 * SCREEN_WIDTH // 4 - PLAYER_WIDTH // 2
        self.player1_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.player2_x = SCREEN_WIDTH // 4 - PLAYER_WIDTH // 2
        self.player2_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.obstacles = []
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        self.last_obstacle_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def update_players(self, keys):
        # Update player 1 (arrow keys)
        if keys[pygame.K_LEFT]:
            self.player1_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player1_x += PLAYER_SPEED

        # Boundary checking for player 1
        if self.player1_x < SCREEN_WIDTH // 2:
            self.player1_x = SCREEN_WIDTH // 2
        elif self.player1_x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.player1_x = SCREEN_WIDTH - PLAYER_WIDTH

        # Update player 2 (WASD keys)
        if keys[pygame.K_a]:
            self.player2_x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.player2_x += PLAYER_SPEED

        # Boundary checking for player 2
        if self.player2_x < 0:
            self.player2_x = 0
        elif self.player2_x > SCREEN_WIDTH // 2 - PLAYER_WIDTH:
            self.player2_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH

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

            # Check collision with player 1
            if (self.player1_x < obstacle_x + OBSTACLE_WIDTH and
                self.player1_x + PLAYER_WIDTH > obstacle_x and
                self.player1_y < obstacle_y + OBSTACLE_HEIGHT and
                self.player1_y + PLAYER_HEIGHT > obstacle_y):
                self.game_over = True
                self.score2 += 1
                self.obstacles.pop(i)

            # Check collision with player 2
            if (self.player2_x < obstacle_x + OBSTACLE_WIDTH and
                self.player2_x + PLAYER_WIDTH > obstacle_x and
                self.player2_y < obstacle_y + OBSTACLE_HEIGHT and
                self.player2_y + PLAYER_HEIGHT > obstacle_y):
                self.game_over = True
                self.score1 += 1
                self.obstacles.pop(i)

            # Remove obstacles that have passed the screen or collided with players
            if obstacle_y > SCREEN_HEIGHT or self.game_over:
                self.obstacles.pop(i)

    def draw_players(self):
        # Draw player 1 (right side)
        pygame.draw.rect(screen, PLAYER_COLOR, (self.player1_x, self.player1_y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Draw player 2 (left side)
        pygame.draw.rect(screen, PLAYER_COLOR, (self.player2_x, self.player2_y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Draw line in the middle
        pygame.draw.line(screen, DARK_GRAY, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

    def draw_obstacles(self):
        for obstacle_x, obstacle_y in self.obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    def draw_scores(self):
        score1_text = font.render(f"Player 1 Score: {self.score1}", True, BLACK)
        score2_text = font.render(f"Player 2 Score: {self.score2}", True, BLACK)
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (SCREEN_WIDTH // 2 + 10, 10))

    def run(self):
        while not self.game_over:
            self.handle_events()

            # Get key states
            keys = pygame.key.get_pressed()

            # Clear the screen with the chosen background color
            screen.fill(LIGHT_BLUE)

            # Update player positions
            self.update_players(keys)

            # Update obstacles and check collisions
            self.update_obstacles()

            # Draw players
            self.draw_players()

            # Draw obstacles
            self.draw_obstacles()

            # Draw scores
            self.draw_scores()

            # Update screen
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
