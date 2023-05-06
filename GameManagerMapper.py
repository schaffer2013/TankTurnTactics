import pygame

# Game Helper
ARROW_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]


class OmnipotentMapper:
    def __init__(self, manager, screenWidth, screenHeight, screenMargin):
        self.gameManager = manager
        self.isActiveArmed = False
        self.isActiveReadyToGive = False
        self.WIDTH = screenWidth
        self.HEIGHT = screenHeight
        self.MARGIN = screenMargin

    def mapMouseEvent(self, event):
        # User clicks the mouse. Get the position
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = pos[0] // (self.WIDTH + self.MARGIN)
        row = pos[1] // (self.HEIGHT + self.MARGIN)
        if self.isActiveArmed:
            self.gameManager.tryShootXY((column, row))

    def mapKeyboardEvent(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
            self.gameManager.increaseActiveTankIndex()
        else:
            success = self.tryActionActiveTank(event)
            if (event.type == pygame.KEYDOWN and not success):
                print("Unavailable action")

    def tryActionActiveTank(self, event):
        success = False
        if (event.type == pygame.KEYDOWN):
            if (not self.gameManager.getActiveTankHasActionPoints()):
                return False
            if (event.key in ARROW_KEYS):
                success = self.tryMoveActiveTank(event.key)
            if (event.key == pygame.K_a):
                self.isActiveArmed = ~self.isActiveArmed
                self.isActiveReadyToGive = False
                success = True
            if (event.key == pygame.K_g):
                self.isActiveReadyToGive = ~self.isActiveReadyToGive
                self.isActiveArmed = False
                success = True
        return success

    def tryMoveActiveTank(self, eventKey):
        if eventKey == pygame.K_RIGHT:
            return self.gameManager.tryMoveActiveTankRight()
        elif eventKey == pygame.K_LEFT:
            return self.gameManager.tryMoveActiveTankLeft()
        elif eventKey == pygame.K_UP:
            return self.gameManager.tryMoveActiveTankUp()
        elif eventKey == pygame.K_DOWN:
            return self.gameManager.tryMoveActiveTankDown()
