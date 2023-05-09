import numpy as np
import NeuralNet
import copy

LAYER_1_NODES = 15


class Brain:
    def __init__(self, numActions):
        self.numActions = numActions
        self.actionsTaken = []
        self.normGameStates = []

    def initWeightsAndBiases(self, exampleNormGameStatus):
        
        self.W1, self.b1, self.W2, self.b2 = NeuralNet.init_params(
            len(exampleNormGameStatus), LAYER_1_NODES, self.numActions)
    
    def reinitWeightsAndBiases(self, params):
        self.W1, self.b1, self.W2, self.b2 = params

    def makeDecision(self, ngs, possibleActions, weightedDecision=False):
        weightedActions, one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(
            self.W1, self.b1, self.W2, self.b2, ngs)
        if weightedDecision:
            weightedAndPossible = []
            for i in range(len(possibleActions)):
                weightedAndPossible.append(possibleActions[i] * weightedActions[i])
            s = sum(weightedAndPossible)
            randomChoice = np.random.rand() * s
            runningValue = 0.0
            for i in range(len(weightedAndPossible)):
                runningValue += weightedAndPossible[i]
                if (runningValue) > randomChoice:
                    self.saveDecision(ngs, i)
                    return i
        else:
            self.saveDecision(ngs, actionIndex)
            return actionIndex

    def saveDecision(self, ngs, actionIndex):
        self.normGameStates.append(ngs)
        self.actionsTaken.append(actionIndex)

    def wiggle(self):
        self.W1 = NeuralNet.wiggleValues(self.W1)
        self.b1 = NeuralNet.wiggleValues(self.b1)
        self.W2 = NeuralNet.wiggleValues(self.W2)
        self.b2 = NeuralNet.wiggleValues(self.b2)

    def learn(self):
        #TODO Add NeuralNet.gradientDesc()
        a = np.array(self.actionsTaken)
        b = np.array(self.normGameStates)
        c = 1

    def exportParams(self):
        return (self.W1, self.b1, self.W2, self.b2)