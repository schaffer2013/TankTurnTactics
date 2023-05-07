import pygame
import jsonpickle
import GameManagerModule
import ScreenHelper
import GameManagerMapper
import AutoClientManager

HANDS_ON = False

# Grid dimensions
GRID_DIM_X = 30
GRID_DIM_Y = 30

# This sets the WIDTH and HEIGHT of each grid location
TOTAL_WIDTH = 1000
TOTAL_HEIGHT = 800
WIDTH = int(TOTAL_WIDTH/GRID_DIM_X)
HEIGHT = int(TOTAL_HEIGHT/GRID_DIM_Y)

# This sets the margin between each cell
MARGIN = int(min(WIDTH, HEIGHT)/10)

# Number of initial tanks
NUM_TANKS = 90

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
timeSinceLastMove = 0
MOVE_DELAY = 100  # ms
PAUSE_DELAY = MOVE_DELAY * 2

manager = GameManagerModule.GameManager(GRID_DIM_X, GRID_DIM_Y, NUM_TANKS)
inputMapper = GameManagerMapper.OmnipotentMapper(
    manager, WIDTH, HEIGHT, MARGIN)
autoClientManager = AutoClientManager.AutoClientManager(manager)

# -------- Main Program Loop -----------
while not done:
    gameStatus = jsonpickle.decode(manager.getFullGameStatus())

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        if HANDS_ON:
            if (event.type == pygame.KEYDOWN):
                inputMapper.mapKeyboardEvent(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                inputMapper.mapMouseEvent(event)
    if not HANDS_ON:
        timeSinceLastMove += clock.get_time()

        if (timeSinceLastMove > MOVE_DELAY and not manager.isPaused):
            autoClientManager.makeAutoDecision()
        if (timeSinceLastMove > MOVE_DELAY + PAUSE_DELAY and manager.isPaused):
            manager.resume()
            timeSinceLastMove = 0

    # Set the screen background
    screen.fill(ScreenHelper.BLACK)

    # Draw the grid
    for r in range(GRID_DIM_Y):
        for c in range(GRID_DIM_X):
            color = ScreenHelper.WHITE
            ScreenHelper.drawCell(c, r, color, screen, MARGIN, HEIGHT, WIDTH)

    showShootable = not HANDS_ON
    showAvailableRange = inputMapper.isActiveArmed or inputMapper.isActiveReadyToGive
    if (HANDS_ON and showAvailableRange) or showShootable:
        for s in gameStatus.getShootableSpots():
            color = ScreenHelper.LIGHT_GRAY
            if inputMapper.isActiveReadyToGive:
                color = ScreenHelper.LIGHT_PURPLE
            ScreenHelper.drawCell(
                s[0], s[1], color, screen, MARGIN, HEIGHT, WIDTH)

    for t in gameStatus.getAliveTanks():
        color = ScreenHelper.INACTIVE
        if t.isActive:
            color = ScreenHelper.ACTIVE
        # region Tank Rendering

        ScreenHelper.drawCell(t.x, t.y, color, screen, MARGIN, HEIGHT, WIDTH)

        font = pygame.font.SysFont('Arial', int(HEIGHT/3))
        biggerFont = pygame.font.SysFont('Arial', int(HEIGHT/2.5))
        tempX = (MARGIN + WIDTH) * t.x + MARGIN
        tempY = (MARGIN + HEIGHT) * t.y + MARGIN

        # Range Render
        ScreenHelper.displayText(screen,
                                 font,
                                 str(t.range),
                                 tempX + int(3*WIDTH/4),
                                 tempY + int(HEIGHT/4))

        # Action point render
        ScreenHelper.displayText(screen,
                                 font,
                                 str(t.actionPoints),
                                 tempX + int(WIDTH/4),
                                 tempY + int(HEIGHT/4))

        # Index Render
        ScreenHelper.displayText(screen,
                                 biggerFont,
                                 str(t.index),
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

    done = done or manager.isAWin
    if manager.isAWin:
        print(f'Tank {manager.winningTank} wins!')

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
