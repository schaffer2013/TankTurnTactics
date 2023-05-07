import numpy as np
import NeuralNet

LAYER_1_NODES = 15


class Brain():
    def __init__(self, numInputs, numActions):
        self.W1, self.b1, self.W2, self.b2 = NeuralNet.init_params(
            numInputs, LAYER_1_NODES, numActions)
    
    def normalizeGameStatus(self, gameStatus):
        return [1]
    
    def makeDecision(self, gameStatus):
        ngs = self.normalizeGameStatus(gameStatus)
        one_hot, actionIndex = NeuralNet.forwardPropAndOneHot(self.W1, self.b1, self.W2, self.b2, ngs)
        return actionIndex
