import jsonpickle

PASS_CMD = 0
MOVE_RIGHT_CMD = 1
MOVE_LEFT_CMD = 2
MOVE_UP_CMD = 3
MOVE_DOWN_CMD = 4
INCREASE_RANGE_CMD = 5

# Using this as a placeholder
FIRST_TANK_SPECIFIC_COMMAND = INCREASE_RANGE_CMD + 1

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

    def mapAction(self, cmdIndex):
        # TODO Replace prints with manager actions
        if (cmdIndex == PASS_CMD):
            print("Pass")
        elif (cmdIndex == MOVE_RIGHT_CMD):
            print("Right")
        elif (cmdIndex == MOVE_LEFT_CMD):
            print("Left")
        elif (cmdIndex == MOVE_UP_CMD):
            print("Up")
        elif (cmdIndex == MOVE_DOWN_CMD):
            print("Down")
        elif (cmdIndex == INCREASE_RANGE_CMD):
            print("Increase Range")
        else:
            # For these tank specific commands,
            # shooting tank[0] will immediately follow
            # the last command that the tank can do to
            # itself (like move). Donating to tank[0]
            # will immediately follow.
            for t in self.gameStatus.getAllTanks():
                if (cmdIndex ==
                    t.index * NUM_TANK_SPEC_COMMANDS +
                    FIRST_TANK_SPECIFIC_COMMAND +
                        SHOOT_THIS_TANK_CMD):
                    print(f'Shoot tank {t.index}')
                    return True
                elif (cmdIndex ==
                      t.index * NUM_TANK_SPEC_COMMANDS +
                      FIRST_TANK_SPECIFIC_COMMAND +
                        DONATE_TO_THIS_TANK_CMD):
                    print(f'Donate to tank {t.index}')
                    return True
            # return False if no case was hit. Will probably need more codes here
            return False
        return True

    def getActionValidations(self):
        activeGameStatus = self.getStatus()
        activeTank = activeGameStatus.getActiveTank()
        # Check for all valid actions for current active tank.
        # This will be an array of bools if the corresponding
        # action from above can be done.
        # Intialize the list of all possible actions
        isValid = [None] * (self.highestCmdIndex + 1)
        
        # Can Pass
        isValid[PASS_CMD] = True

        #region Can Move
        
        #endregion

