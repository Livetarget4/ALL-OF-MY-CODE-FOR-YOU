import random
import time
import os

# Define the game board size
BOARD_WIDTH = 20
BOARD_HEIGHT = 10

# Define characters for game elements
SNAKE_BODY = 'O'
SNAKE_HEAD = '@'
FOOD = '*'
EMPTY_SPACE = ' '

# Game class
class SnakeGame:
    def __init__(self):
        self.snake = [(5, 5), (5, 4), (5, 3)]  # Initial snake position
        self.food = (random.randint(0, BOARD_HEIGHT - 1), random.randint(0, BOARD_WIDTH - 1))  # Random food position
        self.direction = 'RIGHT'  # Initial direction
        self.game_over = False
        self.score = 0

    def print_board(self):
        # Clear screen (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create an empty board
        board = [[EMPTY_SPACE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        # Place the snake on the board
        for x, y in self.snake:
            if (x, y) == self.snake[0]:
                board[x][y] = SNAKE_HEAD  # Head of the snake
            else:
                board[x][y] = SNAKE_BODY  # Body of the snake

        # Place the food on the board
        fx, fy = self.food
        board[fx][fy] = FOOD

        # Print the board
        print(f"Score: {self.score}")
        for row in board:
            print(' '.join(row))

    def change_direction(self):
        new_direction = input("Enter direction (W = Up, S = Down, A = Left, D = Right): ").upper()
        if new_direction in ['W', 'A', 'S', 'D']:
            self.direction = {'W': 'UP', 'S': 'DOWN', 'A': 'LEFT', 'D': 'RIGHT'}[new_direction]

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'UP':
            head_x -= 1
        elif self.direction == 'DOWN':
            head_x += 1
        elif self.direction == 'LEFT':
            head_y -= 1
        elif self.direction == 'RIGHT':
            head_y += 1

        # Check if the snake hits the wall or itself
        if head_x < 0 or head_x >= BOARD_HEIGHT or head_y < 0 or head_y >= BOARD_WIDTH or (head_x, head_y) in self.snake:
            self.game_over = True
            return

        # Add new head to snake
        self.snake.insert(0, (head_x, head_y))

        # Check if snake eats food
        if (head_x, head_y) == self.food:
            self.score += 1
            self.food = (random.randint(0, BOARD_HEIGHT - 1), random.randint(0, BOARD_WIDTH - 1))  # Generate new food
        else:
            # Remove tail if no food eaten
            self.snake.pop()

    def play(self):
        while not self.game_over:
            self.print_board()
            self.change_direction()
            self.move_snake()
            time.sleep(0.1)  # Delay to control game speed

        print("Game Over! Your final score is:", self.score)

# Run the game
if __name__ == '__main__':
    game = SnakeGame()
    game.play()
