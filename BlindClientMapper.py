import jsonpickle

PASS_CMD = 0
MOVE_RIGHT_CMD = 1
MOVE_LEFT_CMD = 2
MOVE_UP_CMD = 3
MOVE_DOWN_CMD = 4

# Using this as a placeholder
FIRST_TANK_SPECIFIC_COMMAND = MOVE_DOWN_CMD + 1

# All commnds that can be done to a tank
SHOOT_THIS_TANK_CMD = 0
DONATE_TO_THIS_TANK_CMD = 1

# This is simply the amount of commands that can be done
NUM_TANK_SPEC_COMMANDS = 2 

class BlindMapper:
    def __init__(self, manager):
        self.gameManager = manager
        self.gameStatus = self.getStatus()
        self.highestCmdIndex = FIRST_TANK_SPECIFIC_COMMAND + \
            (self.gameStatus.numTanks * NUM_TANK_SPEC_COMMANDS) - 1

    def getStatus(self):
        gameStatus = jsonpickle.decode(self.gameManager.getFullGameStatus())
        return gameStatus

    def mapAction(self, index):
        if (index == 0):
            print("Pass")
