import Brain
import FileHelper
import numpy as np

NUM_TANKS = 10
DIM = 15

fileHelper = FileHelper.FileHelper(NUM_TANKS, DIM, Brain.LAYER_1_NODES)


unload = np.array(fileHelper.undumpPossibilities())
ngs = unload[:, 0]
possibilities = unload[:, 1]

brain = Brain.Brain(len(possibilities[0]))
total = 0
npUnload = np.array(unload)

close = True
