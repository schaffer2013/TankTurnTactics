import random
import Strategy


class Client:
    def __init__(self, index):
        self.index = index

    def makeDecision(self, gameStatus, validActions):
        restrictedValidActions = Strategy.pruneValidActions(
            validActions, Strategy.STRATEGY_NO_MOVE)
        return self.makeRandomDecision(restrictedValidActions)

    def makeRandomDecision(self, validActions):
        if validActions.count(True) <= 0:
            print("Uhhhh")
            return
        canDo = False
        while (not canDo):
            actionIndex = random.randint(0, len(validActions)-1)
            canDo = validActions[actionIndex]
        return actionIndex
