import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player attributes
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 100
PLAYER_SPEED = 5
ATTACK_DISTANCE = 50

# Weapon attributes
WEAPON_WIDTH = 20
WEAPON_HEIGHT = 20
WEAPON_SPEED = 5
WEAPON_FREQUENCY = 100  # Weapon spawn frequency in milliseconds

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stick Figure Fight")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y, color, keys):
        self.x = x
        self.y = y
        self.color = color
        self.keys = keys

    def move(self, keys):
        if keys[self.keys[0]]:
            self.x -= PLAYER_SPEED
        if keys[self.keys[1]]:
            self.x += PLAYER_SPEED

        # Boundary checking
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.x = SCREEN_WIDTH - PLAYER_WIDTH

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def attack(self, other_player):
        # Check if other player is within attack range
        if abs(self.x - other_player.x) < ATTACK_DISTANCE:
            return True
        return False

def main():
    player1 = Player(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 20, GREEN, [pygame.K_LEFT, pygame.K_RIGHT])
    player2 = Player(SCREEN_WIDTH - 100 - PLAYER_WIDTH, SCREEN_HEIGHT - PLAYER_HEIGHT - 20, RED, [pygame.K_a, pygame.K_d])

    weapons = []

    score1 = 0
    score2 = 0

    last_weapon_time = pygame.time.get_ticks()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        
        # Clear the screen
        screen.fill(WHITE)

        # Spawn new weapons randomly
        current_time = pygame.time.get_ticks()
        if current_time - last_weapon_time > WEAPON_FREQUENCY:
            weapon_x = random.randint(0, SCREEN_WIDTH - WEAPON_WIDTH)
            weapon_y = 0
            weapons.append((weapon_x, weapon_y))
            last_weapon_time = current_time

        # Update players
        player1.move(keys)
        player2.move(keys)

        # Draw players
        player1.draw()
        player2.draw()

        # Draw weapons
        for weapon in weapons[:]:
            pygame.draw.rect(screen, BLACK, (weapon[0], weapon[1], WEAPON_WIDTH, WEAPON_HEIGHT))
            weapon = (weapon[0], weapon[1] + WEAPON_SPEED)
            if weapon[1] > SCREEN_HEIGHT:
                weapons.remove(weapon)

        # Check if players are attacking each other
        if player1.attack(player2):
            score1 += 1
            print("Player 1 attacked Player 2!")

        if player2.attack(player1):
            score2 += 1
            print("Player 2 attacked Player 1!")

        # Draw scores
        score1_text = font.render(f"Player 1 Score: {score1}", True, BLACK)
        score2_text = font.render(f"Player 2 Score: {score2}", True, BLACK)
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (SCREEN_WIDTH - score2_text.get_width() - 10, 10))

        # Update screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
