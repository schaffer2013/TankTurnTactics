import numpy as np
import NeuralNet
import copy

LAYER_1_NODES = 150


class Brain:
    def __init__(self, numActions):
        self.numActions = numActions
        self.actionsTaken = []
        self.normGameStates = []

    def injectTrainingExperiences(self, actions, ngs):
        a = actions
        b = ngs
        c = 1

    def initWeightsAndBiases(self, exampleNormGameStatus):
        self.W1, self.b1, self.W2, self.b2 = NeuralNet.init_params(
            len(exampleNormGameStatus), LAYER_1_NODES, self.numActions)

    def reinitWeightsAndBiases(self, params):
        self.W1, self.b1, self.W2, self.b2 = params

    def makeDecision(self, ngs, possibleActions, fallbackAction, weightedDecision=False):
        if (False):
            allActionsPossible = [True] * len(possibleActions)
            possibleActions = allActionsPossible

        weightedActions, one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(
            self.W1, self.b1, self.W2, self.b2, ngs)
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
        self.W1 = NeuralNet.wiggleValues(self.W1)
        self.b1 = NeuralNet.wiggleValues(self.b1)
        self.W2 = NeuralNet.wiggleValues(self.W2)
        self.b2 = NeuralNet.wiggleValues(self.b2)

    def learn(self, iterations=1):
        oldParams = (self.W1, self.b1, self.W2, self.b2)
        # TODO Add NeuralNet.gradientDesc()
        a = np.array(self.actionsTaken)
        b = np.array(self.normGameStates)
        if (b.size > 0):
            shaped = b[:, :, 0].transpose()
            (self.W1, self.b1, self.W2, self.b2) = NeuralNet.gradient_descent(
                shaped, a, oldParams, 0.01, 1)
        c = 1

    def learnRaw(self, inputData, outputData, learningRate=0.01, iterations=1):
        oldParams = (self.W1, self.b1, self.W2, self.b2)

        X = np.array(inputData)
        Y = np.array(outputData)
        Y = self.reshape(Y, 2)
        if (Y.size > 0):
            (self.W1, self.b1, self.W2, self.b2) = NeuralNet.gradient_descent(
                X, Y, oldParams, learningRate, iterations, useOneHot=False)
        c = 1

    def reshape(self, data, neededDims):
        while data.ndim < neededDims:
            data = np.expand_dims(data, axis=data.ndim)
        return data

    def exportParams(self):
        return (self.W1, self.b1, self.W2, self.b2)
