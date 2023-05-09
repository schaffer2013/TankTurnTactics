import random
import Strategy
from Brain import Brain


class Client:
    def __init__(self, index, numPossibleActions):
        self.index = index
        self.brain = Brain(numPossibleActions)

    def makeDecision(self, gameStatus, possibleActions):
        return self.brain.makeDecision(gameStatus, possibleActions, True) # returns actionIndex


    # def makeDecision(self, gameStatus, validActions):
    #     restrictedValidActions = Strategy.pruneValidActions(
    #         validActions, Strategy.STRATEGY_NO_DONATE)
    #     return self.makeRandomDecision(restrictedValidActions)

    def makeRandomDecision(self, validActions):
        if validActions.count(True) <= 0:
            print("Uhhhh")
            return
        canDo = False
        while (not canDo):
            actionIndex = random.randint(0, len(validActions)-1)
            canDo = validActions[actionIndex]
        return actionIndex
