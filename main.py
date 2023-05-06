import pygame
import copy
from Tank import Tank
import GameManagerModule
import ScreenHelper
import GameManagerMapper

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 42
HEIGHT = 35

# This sets the margin between each cell
MARGIN = 5

# Grid dimensions
GRID_DIM_X = 10
GRID_DIM_Y = 10

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(GRID_DIM_Y):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(GRID_DIM_X):
        grid[row].append(0)  # Append a cell

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(WIDTH+MARGIN)*GRID_DIM_X+MARGIN,
               (HEIGHT+MARGIN)*GRID_DIM_Y+MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Tank Turn Tactics")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

manager = GameManagerModule.GameManager(GRID_DIM_X, GRID_DIM_Y, 5)
mapper = GameManagerMapper.KeyboardMapper(manager)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if (event.type == pygame.KEYDOWN):
            mapper.mapKeyboardEvent(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            if mapper.isActiveArmed:
                manager.tryShoot((column, row))

    # Set the screen background
    screen.fill(ScreenHelper.BLACK)

    # Draw the grid
    for r in range(GRID_DIM_Y):
        for c in range(GRID_DIM_X):
            color = ScreenHelper.WHITE
            ScreenHelper.drawCell(c, r, color, screen, MARGIN, HEIGHT, WIDTH)

    if mapper.isActiveArmed:
        for s in manager.getShootableSpots():
            color = ScreenHelper.LIGHT_GRAY
            ScreenHelper.drawCell(s[0], s[1], color, screen, MARGIN, HEIGHT, WIDTH)
    
    for t in manager.getAliveTanks():
        color = ScreenHelper.INACTIVE
        if t.isActive:
            color = ScreenHelper.ACTIVE
        # region Tank Rendering

        ScreenHelper.drawCell(t.x, t.y, color, screen, MARGIN, HEIGHT, WIDTH)

        font = pygame.font.SysFont('Arial', int(HEIGHT/3))
        tempX = (MARGIN + WIDTH) * t.x + MARGIN
        tempY = (MARGIN + HEIGHT) * t.y + MARGIN
        # Index Render
        ScreenHelper.displayText(screen,
                                    font,
                                    str(t.actionPoints),
                                    tempX + int(3*WIDTH/4),
                                    tempY + int(HEIGHT/4))
        
        # Action point render
        ScreenHelper.displayText(screen,
                                    font,
                                    str(t.index),
                                    tempX + int(WIDTH/4),
                                    tempY + int(HEIGHT/4))
        
        # Range Render
        ScreenHelper.displayText(screen,
                                    font,
                                    str(t.range),
                                    tempX + int(WIDTH/2),
                                    tempY + int(3*HEIGHT/4))

        # Extra Live Render
        circleLeft = tempX
        circleRight = tempX + WIDTH
        circleBottom = tempY + HEIGHT
        circleRadius = min(WIDTH/3, HEIGHT/3)/2
        if (t.extra_lives > 0):
            ScreenHelper.drawRedCircle(screen,
                (circleLeft, circleBottom),
                circleRadius,
                draw_top_right=True)
        if (t.extra_lives > 1):
            ScreenHelper.drawRedCircle(screen,
                (circleRight, circleBottom),
                circleRadius,
                draw_top_left=True)
                            
            # endregion

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
