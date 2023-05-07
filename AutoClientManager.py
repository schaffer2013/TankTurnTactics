import BlindClientMapper
from AutoClient import Client


class AutoClientManager:
    def __init__(self, manager):
        self.mapper = BlindClientMapper.BlindMapper(manager)
        gameStatus = self.mapper.getStatus()

        self.allClients = []
        for i in range(gameStatus.numTanks):
            self.allClients.append(Client(i))

    def makeAutoDecision(self):
        gameStatus = self.mapper.getStatus()
        possibleActions = self.mapper.getActionValidations()
        activeClient = self.allClients[gameStatus.activeTankIndex]

        action = activeClient.makeRandomDecision(gameStatus, possibleActions)
        self.mapper.mapAction(action)
