import PCF8591 as ADC
import time

def setup():
    ADC.setup(0x48)  # Setup PCF8591
    global state

def get_joystick_position():
    x = ADC.read(0)  # Read joystick x-axis
    y = ADC.read(1)  # Read joystick y-axis
    return x, y

# Game loop
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
            if (dot_x + DOT_SIZE >= obstacle_x and dot_x <= obstacle_x + OBSTACLE_SIZE and dot_y + DOT_SIZE >= obstacle_y and dot_y <= obstacle_y + OBSTACLE_SIZE):
                end = time.time()
                score = round(end - start)
                init(0x27, 1)
                write(0, 0,  username+ ' Score') #THIS SPACE IS TO DISPLAY ENDING SCREEN
                write(0, 1, str(score))
                running = False
               

    # Get joystick position
    joystick_x, joystick_y = get_joystick_position()

    # Move the dot based on joystick position
    dot_x += int((joystick_x - 125) / 15)  # Adjust these values based on your joystick sensitivity
    dot_y += int((joystick_y - 125) / 15)  # Adjust these values based on your joystick sensitivity

    # Draw the dot (player)
    pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), DOT_SIZE)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

