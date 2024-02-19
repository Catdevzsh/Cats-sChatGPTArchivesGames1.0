import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Pac-Man')

# Maze setup with 'd' for dots
maze_layout = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.d............WW.dW",
    "W.WWWW.WWWWW.WW.WWWW",
    "WdWWWW.WWWWW.WW.WWWW",
    "Wd....WW...WW.....dW",
    "W.WWWWWWWWWWWW.WWWW",
    "W........P......WdW",  # Pac-Man's starting position
    "WWWWWWWWWWWWWWWWWWWW"
]

# Variables initialization
maze_row_height = screen_height // len(maze_layout)
maze_column_width = screen_width // len(maze_layout[0])
wall_color = (0, 0, 255)  # Blue walls
dot_color = (255, 255, 255)  # White dots
pacman_color = (255, 255, 0)  # Yellow
pacman_x, pacman_y = 0, 0  # Set based on 'P'
pacman_direction = 'right'
pacman_speed = maze_column_width // 10
pacman_radius = min(maze_row_height, maze_column_width) // 4
pacman_open_angle = 45
score = 0  # Track the score
ghost_directions = ['right', 'left', 'up', 'down']

# Find Pac-Man's starting position
for row_index, row in enumerate(maze_layout):
    for col_index, cell in enumerate(row):
        if cell == 'P':
            pacman_x = col_index * maze_column_width + maze_column_width // 2
            pacman_y = row_index * maze_row_height + maze_row_height // 2
            # Remove 'P' after setting Pac-Man's position
            maze_layout[row_index] = maze_layout[row_index][:col_index] + '.' + maze_layout[row_index][col_index+1:]

# Ghost setup
ghost_x, ghost_y = screen_width // 4, screen_height // 4  # Adjust as needed
ghost_color = (255, 0, 0)
ghost_speed = pacman_speed // 2
ghost_direction = random.choice(ghost_directions)

running = True
clock = pygame.time.Clock()

def is_wall(x, y):
    row = y // maze_row_height
    col = x // maze_column_width
    return maze_layout[row][col] == 'W'

def change_ghost_direction():
    global ghost_direction
    possible_directions = ghost_directions.copy()
    possible_directions.remove(ghost_direction)  # Avoid immediate reversal
    ghost_direction = random.choice(possible_directions)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman_direction = 'right'
            elif event.key == pygame.K_LEFT:
                pacman_direction = 'left'
            elif event.key == pygame.K_UP:
                pacman_direction = 'up'
            elif event.key == pygame.K_DOWN:
                pacman_direction = 'down'

    # Pac-Man Movement with wall collision
    next_x, next_y = pacman_x, pacman_y
    if pacman_direction == 'right':
        next_x += pacman_speed
    elif pacman_direction == 'left':
        next_x -= pacman_speed
    elif pacman_direction == 'up':
        next_y -= pacman_speed
    elif pacman_direction == 'down':
        next_y += pacman_speed

    if not is_wall(next_x, next_y):
        pacman_x, pacman_y = next_x, next_y
        row, col = pacman_y // maze_row_height, pacman_x // maze_column_width
        if maze_layout[row][col] == 'd':
            score += 10  # Increase score
            maze_layout[row] = maze_layout[row][:col] + '.' + maze_layout[row][col+1:]  # Remove 'd'

    # Ghost Movement (improved AI)
    ghost_next_x, ghost_next_y = ghost_x, ghost_y
    if ghost_direction == 'right':
        ghost_next_x += ghost_speed
    elif ghost_direction == 'left':
        ghost_next_x -= ghost_speed
    elif ghost_direction == 'up':
        ghost_next_y -= ghost_speed
    elif ghost_direction == 'down':
        ghost_next_y += ghost_speed

    if is_wall(ghost_next_x, ghost_next_y):  # Change direction if about to hit a wall
        change_ghost_direction()
    else:
        ghost_x, ghost_y = ghost_next_x, ghost_next_y

    # Clear screen and draw everything
    screen.fill((0, 0, 0))
    for row_index, row in enumerate(maze_layout):
        for col_index, cell in enumerate(row):
            x, y = col_index * maze_column_width, row_index * maze_row_height
            if cell == 'W':
                pygame.draw.rect(screen, wall_color, (x, y, maze_column_width, maze_row_height))
            elif cell == 'd':
                pygame.draw.circle(screen, dot_color, (x + maze_column_width // 2, y + maze_row_height // 2), pacman_radius // 2)

    # Draw Pac-Man and Ghost
    start_angle = math.radians(pacman_open_angle if pacman_direction in ['left', 'up'] else 0)
    end_angle = math.radians(360 - pacman_open_angle if pacman_direction in ['right', 'down'] else 180)
    pygame.draw.arc(screen, pacman_color, (pacman_x - pacman_radius, pacman_y - pacman_radius, 2 * pacman_radius, 2 * pacman_radius), start_angle, end_angle, pacman_radius)
    pygame.draw.circle(screen, ghost_color, (ghost_x, ghost_y), pacman_radius // 2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
