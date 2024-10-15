import pygame
pygame.init()

# Create the game window
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

# Initialize rectangle properties
x = 50
y = 50
width = 40
height = 60
vel = 5

# Control variable for the game loop
run = True

while run:
    pygame.time.delay(100)

    # Handle events, such as window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get the state of the keys
    keys = pygame.key.get_pressed()

    # Move the rectangle with arrow keys
    if keys[pygame.K_LEFT] and x > vel:  # Ensure the rectangle stays within the window
        x -= vel
    if keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
    if keys[pygame.K_UP] and y > vel:
        y -= vel
    if keys[pygame.K_DOWN] and y < 500 - height - vel:
        y += vel

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if the left mouse button is pressed
    if pygame.mouse.get_pressed()[0]:  # Index 0 corresponds to the left mouse button
        x, y = mouse_pos  # Move the rectangle to the mouse position

    # Fill the window with black
    win.fill((0, 0, 0))

    # Draw the rectangle at the updated position
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))

    # Update the display to reflect changes
    pygame.display.update()

# Quit Pygame when done
pygame.quit()
