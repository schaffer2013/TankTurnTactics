import numpy as np
import NeuralNet
import copy

#LAYER_1_NODES = 150


class Brain:
    def __init__(self, numActions, numNodesInLayers=[150]):
        self.numActions = numActions
        self.actionsTaken = []
        self.normGameStates = []
        self.numNodesInLayers = numNodesInLayers
        self.weightsAndBiases = []
        self.lastSse = 10 ** 15

    def injectTrainingExperiences(self, actions, ngs):
        a = actions
        b = ngs
        c = 1

    def initWeightsAndBiases(self, exampleNormGameStatus):
        self.weightsAndBiases = NeuralNet.init_params(
            len(exampleNormGameStatus), self.numNodesInLayers, self.numActions)

    def reinitWeightsAndBiases(self, params):
        self.weightsAndBiases = params

    def makeDecision(self, ngs, possibleActions, fallbackAction, weightedDecision=False):
        if (False):
            allActionsPossible = [True] * len(possibleActions)
            possibleActions = allActionsPossible

        weightedActions, one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(
            self.weightsAndBiases, ngs)
        if weightedDecision:
            weightedAndPossible = []
            for i in range(len(possibleActions)):
                weightedAndPossible.append(
                    possibleActions[i] * weightedActions[i])
            s = sum(weightedAndPossible)
            if (s <= 0.0):
                raise Exception("This is bad")
                actionIndex = fallbackAction
                self.saveDecision(ngs, actionIndex)
                return actionIndex
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
        for i in range(len(self.weightsAndBiases)):
            self.weightsAndBiases[i][NeuralNet.W_INDEX] = NeuralNet.wiggleValues(self.weightsAndBiases[i][NeuralNet.W_INDEX])
            self.weightsAndBiases[i][NeuralNet.B_INDEX] = NeuralNet.wiggleValues(self.weightsAndBiases[i][NeuralNet.B_INDEX])

    def learn(self, iterations=1):
        oldParams = self.weightsAndBiases
        # TODO Add NeuralNet.gradientDesc()
        a = np.array(self.actionsTaken)
        b = np.array(self.normGameStates)
        if (b.size > 0):
            shaped = b[:, :, 0].transpose()
            (self.weightsAndBiases, _, _) = NeuralNet.gradient_descent(
                shaped, a, oldParams, 0.005, 10)
        c = 1

    def learnRaw(self, inputData, outputData, learningRate=0.0005, iterations=1):
        LR = 0.001
        for i in range(iterations):
            oldParams = self.weightsAndBiases

            X = np.array(inputData).transpose()
            for i in range(len(X)):
                if len(X[i]) != len(X[0]):
                    raise Exception("fsdfs")
            Y = np.array(outputData)
            Y = NeuralNet.reshape(Y, 2)
            if (Y.size > 0):
                (self.weightsAndBiases, sse, A2) = NeuralNet.gradient_descent(
                    X, Y, oldParams, LR, iterations, useOneHot=False)
                if self.lastSse < sse:
                    LR = LR / 2.
                    if LR < 0.000001:
                        return self.weightsAndBiases
                self.lastSse = sse

    def exportParams(self):
        return self.weightsAndBiases
