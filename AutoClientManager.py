import random
import BlindClientMapper
from AutoClient import Client

# Use this to export a subset of possibilities
CHANCE_FOR_EXAMPLE = 0.0


class AutoClientManager:
    def __init__(self, manager, nodeCounts, baselineWeights=None):
        self.mapper = BlindClientMapper.BlindMapper(manager)
        gameStatus = self.mapper.getStatus()

        self.allClients = []
        for i in range(gameStatus.numTanks):
            self.allClients.append(
                Client(i, self.mapper.highestCmdIndex + 1, nodeCounts))
            if baselineWeights == None:
                ngs = self.allClients[i].normalizeGameStatus(gameStatus)
                self.allClients[i].brain.initWeightsAndBiases(ngs)
            else:
                self.allClients[i].brain.reinitWeightsAndBiases(
                    baselineWeights)

        self.trainingPossibleActions = []

    def reInit(self, newGen):
        self.allClients = []
        hiddenNodeCounts = self.getNodeCountFromParams(self.allSavedClientParams[0])
        for i in range(len(newGen)):
            self.allClients.append(Client(i, self.mapper.highestCmdIndex + 1, hiddenNodeCounts))
            # Reinit the w+b as params from the survivors from the previous gen
            brain = self.allClients[i].brain
            brain.reinitWeightsAndBiases(self.allSavedClientParams[newGen[i]])
            brain.wiggle()
        a = 1

    def getNodeCountFromParams(self, savedParam):
        hiddenNodeCounts = []
        for p in self.allSavedClientParams[0]:
            hiddenNodeCounts.append(p[0].shape[0]) # get the previous sizes from the brain itself.
        hiddenNodeCounts.pop() # Remove the output layer amount
        return hiddenNodeCounts

    def exportWeights(self):
        gameStatus = self.mapper.getStatus()
        winnerIndex = gameStatus.winningTank
        self.allSavedClientParams = []
        for i in range(len(self.allClients)):
            self.allClients[i].brain.learn()
            self.allSavedClientParams.append(
                self.allClients[i].brain.exportParams())
        return self.allSavedClientParams[winnerIndex]

    def exportTrainingSet(self):
        l = len(self.trainingPossibleActions)
        return self.trainingPossibleActions

    def makeAutoDecision(self):
        gameStatus = self.mapper.getStatus()
        possibleActions = self.mapper.getActionValidations()
        activeClient = self.allClients[gameStatus.activeTankIndex]

        action, ngs = activeClient.makeDecision(
            gameStatus, possibleActions, BlindClientMapper.WITHER_CMD)
        if (random.random() < CHANCE_FOR_EXAMPLE):
            self.trainingPossibleActions.append([ngs, possibleActions])

        if (possibleActions[action]):
            self.mapper.mapAction(action)
        else:
            # if the client chooses an action they can't do,
            # replace with a wither as punishment
            self.mapper.mapAction(BlindClientMapper.WITHER_CMD)
