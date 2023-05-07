import random


class Client:
    def __init__(self, index):
        self.index = index

    def makeRandomDecision(self, gameStatus, validActions):
        if validActions.count(True) <= 0:
            print("Uhhhh")
            return
        canDo = False
        while (not canDo):
            actionIndex = random.randint(0, len(validActions)-1)
            canDo = validActions[actionIndex]
        return actionIndex
