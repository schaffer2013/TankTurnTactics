import random
import numpy as np
import copy
import Strategy
from Brain import Brain


class Client:
    def __init__(self, index, numPossibleActions, nodeCounts):
        self.index = index
        self.brain = Brain(numPossibleActions, nodeCounts, Strategy.STRATEGY_SIT_AND_SHOOT_ON_SIGHT if index == 0 else Strategy.STRATEGY_NO_RESTRICTIONS)

    def makeDecision(self, gameStatus, possibleActions, fallbackAction):
        ngs = self.normalizeGameStatus(gameStatus)
        # returns actionIndex
        _, actionIndex = self.brain.makeDecision(
            ngs, possibleActions, fallbackAction, True)
        return actionIndex, ngs

    def normalizeGameStatus(self, gameStatus):
        def myFunc(e):
            return (e.index - gameStatus.activeTankIndex) % gameStatus.numTanks
        # Stub out:
        # For each tank, starting with active and looping
        # to the tank that just acted: (not absolute index!)
        #   -isAlive (bool) (not necessary for active)
        #   -extraLives/2.0
        #   -positionX/DIM_X
        #   -positionY/DIM_Y
        #   -min(range/max(DIM_X, DIM_Y), 1.0)
        #   -min(actionPoints/10.0, 1.0) * isAlive
        # Just once:
        #   -1/max(DIM_X, DIM_Y)
        allParams = []
        allTanksCopy = copy.deepcopy(gameStatus.AllTanks)
        allTanksCopy.sort(key=myFunc)
        if (allTanksCopy[0].index != gameStatus.activeTankIndex):
            reaction = "Yell"
        for t in allTanksCopy:
            allParams.extend(self.normalizeTankHelper(
                t, gameStatus.dimX, gameStatus.dimY))
        allParams.append(1.0/max(gameStatus.dimX, gameStatus.dimY))
        return np.transpose(np.array([allParams]))

    def normalizeTankHelper(self, tank, dimX, dimY):
        maxDim = (max(dimX, dimY))
        tankParams = []
        tankParams.append(tank.isAlive * 1.0)
        tankParams.append(tank.extra_lives / 2.0)
        tankParams.append(float(tank.x) / dimX)
        tankParams.append(float(tank.y) / dimY)
        tankParams.append(min(float(tank.range) / maxDim, 1.0))
        tankParams.append(min(float(tank.actionPoints) /
                          10.0, 1.0) * float(tank.isAlive))
        return tankParams

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
