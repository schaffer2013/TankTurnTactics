import pickle
import os

POSS_FILE_PREFIX = 'POSS-'
BASE_FILE_PREFIX = 'BASE-'


class FileHelper:
    def __init__(self, numTanks, dim, L1Nodes):
        self.numTanks = numTanks
        self.dim = dim
        self.L1Nodes = L1Nodes

    def getFileNameWeights(self):
        return(f'weights-{str(self.numTanks)}tanks-{str(self.dim)}dim-{str(self.L1Nodes)}L1Nodes.pkl')

    def getFileNamePossibilities(self):
        return POSS_FILE_PREFIX + self.getFileNameWeights()

    def getFileNameBaseWeights(self):
        return BASE_FILE_PREFIX + self.getFileNameWeights()

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
        file = open(fileName, 'rb')
        return pickle.load(file)
