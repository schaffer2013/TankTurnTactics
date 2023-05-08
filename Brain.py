import numpy as np
import NeuralNet
import copy

LAYER_1_NODES = 60


class Brain:
    def __init__(self, numActions):
        self.numActions = numActions

    def initWeightsAndBiases(self, exampleGameStatus):
        ngs = self.normalizeGameStatus(exampleGameStatus)
        self.W1, self.b1, self.W2, self.b2 = NeuralNet.init_params(
            len(ngs), LAYER_1_NODES, self.numActions)
    
    def reinitWeightsAndBiases(self, params):
        self.W1, self.b1, self.W2, self.b2 = params

    def makeDecision(self, gameStatus, weightedDecision=False):
        ngs = self.normalizeGameStatus(gameStatus)
        weightedActions, one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(
            self.W1, self.b1, self.W2, self.b2, ngs)
        if weightedDecision:
            randomChoice = np.random.rand()
            runningValue = 0.0
            for i in range(len(weightedActions)):
                runningValue += weightedActions[i]
                if (runningValue) > randomChoice:
                    return i
        return actionIndex

    def wiggle(self):
        self.W1 = NeuralNet.wiggleValues(self.W1)
        self.b1 = NeuralNet.wiggleValues(self.b1)
        self.W2 = NeuralNet.wiggleValues(self.W2)
        self.b2 = NeuralNet.wiggleValues(self.b2)

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

    def exportParams(self):
        return (self.W1, self.b1, self.W2, self.b2)