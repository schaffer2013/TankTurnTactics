import jsonpickle

DEBUG = False

PASS_CMD = 0
MOVE_RIGHT_CMD = 1
MOVE_LEFT_CMD = 2
MOVE_UP_CMD = 3
MOVE_DOWN_CMD = 4
INCREASE_RANGE_CMD = 5
WITHER_CMD = 6

# Using this as a placeholder
FIRST_TANK_SPECIFIC_COMMAND = WITHER_CMD + 1

# All commnds that can be done to a tank
SHOOT_THIS_TANK_CMD = 0
DONATE_TO_THIS_TANK_CMD = 1

# This is simply the amount of commands that can be done
NUM_TANK_SPEC_COMMANDS = 2

class BlindMapper:
    def __init__(self, manager):
        self.gameManager = manager
        gameStatus = self.getStatus()
        self.highestCmdIndex = FIRST_TANK_SPECIFIC_COMMAND + \
            (gameStatus.numTanks * NUM_TANK_SPEC_COMMANDS) - 1

    def getStatus(self):
        gameStatus = jsonpickle.decode(self.gameManager.getFullGameStatus())
        #gameStatus.reInit()
        return gameStatus

    def mapAction(self, cmdIndex):
        # TODO Replace prints with manager actions
        if self.gameManager.checkWin():
            return True
        if (cmdIndex == PASS_CMD):
            self.printDebug("Pass")
            self.gameManager.increaseActiveTankIndex()
        elif (cmdIndex == MOVE_RIGHT_CMD):
            self.printDebug("Right")
            self.gameManager.tryMoveActiveTankRight()
        elif (cmdIndex == MOVE_LEFT_CMD):
            self.printDebug("Left")
            self.gameManager.tryMoveActiveTankLeft()
        elif (cmdIndex == MOVE_UP_CMD):
            self.printDebug("Up")
            self.gameManager.tryMoveActiveTankUp()
        elif (cmdIndex == MOVE_DOWN_CMD):
            self.printDebug("Down")
            self.gameManager.tryMoveActiveTankDown()
        elif (cmdIndex == INCREASE_RANGE_CMD):
            self.printDebug("Increase Range")
            self.gameManager.increaseActiveTankRange()
        elif (cmdIndex == WITHER_CMD):
            self.printDebug("Wither :(")
            self.gameManager.witherActiveTank()
        else:
            # For these tank specific commands,
            # shooting tank[0] will immediately follow
            # the last command that the tank can do to
            # itself (like move). Donating to tank[0]
            # will immediately follow.
            gameStatus = self.getStatus()
            for t in gameStatus.getAllTanks():
                if (cmdIndex == self.getShootCmdIndex(t.index)):
                    self.printDebug(f'Shoot tank {t.index}')
                    self.gameManager.tryShootOrDonate(t.index, True)
                    return True
                elif (cmdIndex == self.getDonateCmdIndex(t.index)):
                    self.printDebug(f'Donate to tank {t.index}')
                    self.gameManager.tryShootOrDonate(t.index, False)
                    return True
            # return False if no case was hit. Will probably need more codes here
            return False
        return True

    def getActionValidations(self):
        gameStatus = self.getStatus()
        activeTank = gameStatus.getActiveTank()
        # Check for all valid actions for current active tank.
        # This will be an array of bools if the corresponding
        # action from above can be done.
        # Intialize the list of all possible actions
        isValid = [None] * (self.highestCmdIndex + 1)

        # Can Pass
        isValid[PASS_CMD] = True

        # Can Move
        isValid[MOVE_RIGHT_CMD] = gameStatus.canMoveActiveTank(1, 0)
        isValid[MOVE_LEFT_CMD] = gameStatus.canMoveActiveTank(-1, 0)
        isValid[MOVE_UP_CMD] = gameStatus.canMoveActiveTank(0, -1)
        isValid[MOVE_DOWN_CMD] = gameStatus.canMoveActiveTank(0, 1)

        # Can Increase Range
        isValid[INCREASE_RANGE_CMD] = gameStatus.dimX > activeTank.range

        # Can Wither
        isValid[WITHER_CMD] = True

        # region "To other tank" commands
        # The ability to shoot and donate both are based on the range
        # of the active tank, so they should always be the same. You
        # can't shoot or donate to yourself.
        for t in gameStatus.getAllTanks():
            canHit = False
            if (t.index is not activeTank.index):
                canHit = gameStatus.canShootOrDonate(t.index)

            isValid[self.getShootCmdIndex(t.index)] = canHit
            isValid[self.getDonateCmdIndex(t.index)] = False
        # endregion
        return isValid

    # region Helpers
    def getShootCmdIndex(self, tankIndex):
        return tankIndex * NUM_TANK_SPEC_COMMANDS + \
            FIRST_TANK_SPECIFIC_COMMAND + \
            SHOOT_THIS_TANK_CMD

    def getDonateCmdIndex(self, tankIndex):
        return tankIndex * NUM_TANK_SPEC_COMMANDS + \
            FIRST_TANK_SPECIFIC_COMMAND + \
            DONATE_TO_THIS_TANK_CMD
    def printDebug(self, string):
        if DEBUG:
            print(string)
    # endregion
