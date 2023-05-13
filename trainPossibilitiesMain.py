import Brain
import FileHelper
import numpy as np

NUM_TANKS = 10
DIM = 15

fileHelper = FileHelper.FileHelper(NUM_TANKS, DIM, Brain.LAYER_1_NODES)


unload = np.array(fileHelper.undumpPossibilities())
np.random.shuffle(unload)
ngs = unload[:, 0]
possibilities = unload[:, 1]

brain = Brain.Brain(len(possibilities[0]))
brain.initWeightsAndBiases(ngs[0])

brain.learnRaw(ngs[0], possibilities[0])
close = True
