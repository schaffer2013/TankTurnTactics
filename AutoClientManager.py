import BlindClientMapper
from AutoClient import Client


class AutoClientManager:
    def __init__(self, manager):
        self.mapper = BlindClientMapper.BlindMapper(manager)
        gameStatus = self.mapper.getStatus()

        self.allClients = []
        for i in range(gameStatus.numTanks):
            self.allClients.append(Client(i, self.mapper.highestCmdIndex + 1))
            ngs = self.allClients[i].normalizeGameStatus(gameStatus)
            self.allClients[i].brain.initWeightsAndBiases(ngs)

    def reInit(self, newGen):
        self.allClients = []
        for i in range(len(newGen)):
            self.allClients.append(Client(i, self.mapper.highestCmdIndex + 1))
            # Reinit the w+b as params from the survivors from the previous gen
            brain = self.allClients[i].brain
            brain.reinitWeightsAndBiases(self.allSavedClientParams[newGen[i]])
            brain.wiggle()
        a = 1

    def exportWeights(self):
        gameStatus = self.mapper.getStatus()
        winnerIndex = gameStatus.winningTank
        self.allSavedClientParams = []
        for i in range(len(self.allClients)):
            self.allClients[i].brain.learn()
            self.allSavedClientParams.append(
                self.allClients[i].brain.exportParams())
        return self.allSavedClientParams[winnerIndex]

    def makeAutoDecision(self):
        gameStatus = self.mapper.getStatus()
        possibleActions = self.mapper.getActionValidations()
        activeClient = self.allClients[gameStatus.activeTankIndex]

        action = activeClient.makeDecision(gameStatus, possibleActions, BlindClientMapper.WITHER_CMD)
        if (possibleActions[action]):
            self.mapper.mapAction(action)
        else:
            # if the client chooses an action they can't do,
            # replace with a wither as punishment
            self.mapper.mapAction(BlindClientMapper.WITHER_CMD)
