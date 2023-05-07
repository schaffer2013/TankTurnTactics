import numpy as np
import NeuralNet

LAYER_1_NODES = 15


class Brain:
    def __init__(self, numActions):
        self.numActions = numActions

    def reInitWeightsAndBiases(self, exampleGameStatus):
        ngs = self.normalizeGameStatus(exampleGameStatus)
        self.W1, self.b1, self.W2, self.b2 = NeuralNet.init_params(
            len(ngs), LAYER_1_NODES, self.numActions)

    def makeDecision(self, gameStatus):
        ngs = self.normalizeGameStatus(gameStatus)
        one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(
            self.W1, self.b1, self.W2, self.b2, ngs)
        return actionIndex

    def wiggle(self):
        self.W1 = NeuralNet.wiggleValues(self.W1)
        self.b1 = NeuralNet.wiggleValues(self.b1)
        self.W2 = NeuralNet.wiggleValues(self.W2)
        self.b2 = NeuralNet.wiggleValues(self.b2)

    def normalizeGameStatus(self, gameStatus):
        # TODO make all inputs in a [0.0, 1.0] range
        # Currently dummy data!!!!
        return np.random.randn(4,1)
