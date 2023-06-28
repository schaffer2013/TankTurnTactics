import pickle
import os

POSS_FILE_PREFIX = 'POSS-'
BASE_FILE_PREFIX = 'BASE-'
WEIGHTS_FOLDER = 'saved weights'


class FileHelper:
    def __init__(self, numTanks, dim, nodeCounts):
        self.numTanks = numTanks
        self.dim = dim
        self.nodeCounts = nodeCounts

        isExist = os.path.exists(WEIGHTS_FOLDER)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(WEIGHTS_FOLDER)
            print("The new directory is created!")

    def getFileNameWeights(self):
        runningString = f'weights-{str(self.numTanks)}tanks-{str(self.dim)}dim'#{str(self.L1Nodes)}L1Nodes.pkl'
        for i in range(len(self.nodeCounts)):
            runningString += f'-{str(self.nodeCounts[i])}L{i}Nodes'
        runningString += '.pkl'
        return (f'{WEIGHTS_FOLDER}/{runningString}')

    def getFileNamePossibilities(self):
        return POSS_FILE_PREFIX + self.getFileNameWeights()

    def getFileNameBaseWeights(self):
        return (f'{WEIGHTS_FOLDER}/{BASE_FILE_PREFIX + self.getFileNameWeights()}')

    def fileDump(self, fileName, data):
        with open(fileName, 'wb') as file:
            # A new file will be created
            pickle.dump(data, file)

    def fileDumpWeights(self, data):
        self.fileDump(self.getFileNameWeights(), data)

    def fileDumpBaseWeights(self, data):
        self.fileDump(self.getFileNameBaseWeights(), data)

    def fileDumpPossibilities(self, data):
        self.fileDump(self.getFileNamePossibilities(), data)

    def weightFileExists(self):
        return os.path.isfile(self.getFileNameWeights())

    def possibilitiesFileExists(self):
        return os.path.isfile(self.getFileNamePossibilities())

    def undumpWeights(self):
        return self.undump(self.getFileNameWeights())
    
    def undumpBaseWeights(self):
        return self.undump(self.getFileNameBaseWeights())

    def undumpPossibilities(self):
        return self.undump(self.getFileNamePossibilities())

    def undump(self, fileName):
        if not os.path.isfile(fileName):
            return None
        file = open(fileName, 'rb')
        return pickle.load(file)
