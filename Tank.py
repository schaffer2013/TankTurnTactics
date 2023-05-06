INITIAL_ACTION_POINTS = 2
INITIAL_EXTRA_LIVES = 2
INITIAL_RANGE = 2

class Tank:

    def __init__(self, index, initialX, initialY):
        self.index = index
        self.x = initialX
        self.y = initialY
        self.actionPoints = INITIAL_ACTION_POINTS
        self.extra_lives = INITIAL_EXTRA_LIVES
        self.range = INITIAL_RANGE
        self.isActive = False
        self.isAlive = True