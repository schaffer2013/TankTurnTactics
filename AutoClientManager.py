import BlindClientMapper
from AutoClient import Client


class AutoClientManager:
    def __init__(self, manager):
        self.mapper = BlindClientMapper.BlindMapper(manager)
        gameStatus = self.mapper.getStatus()

        self.allClients = []
        for i in range(gameStatus.numTanks):
            self.allClients.append(Client(i, self.mapper.highestCmdIndex + 1))
            self.allClients[i].brain.reInitWeightsAndBiases(gameStatus)

    def makeAutoDecision(self):
        gameStatus = self.mapper.getStatus()
        possibleActions = self.mapper.getActionValidations()
        activeClient = self.allClients[gameStatus.activeTankIndex]

        action = activeClient.makeDecision(gameStatus)
        if (possibleActions[action]):
            self.mapper.mapAction(action)
        else:
            # if the client chooses an action they can't do, 
            # replace with a wither as punishment
            self.mapper.mapAction(BlindClientMapper.WITHER_CMD)
