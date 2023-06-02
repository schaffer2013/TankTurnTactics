import random
import Brain
import FileHelper
import numpy as np

NUM_TANKS = 10
DIM = 15

fileHelper = FileHelper.FileHelper(NUM_TANKS, DIM, Brain.LAYER_1_NODES)

ngs = []
possibilities = []

unload = fileHelper.undumpPossibilities()
random.shuffle(unload)

for u in unload:
    ngs.append(u[0])
    possibilities.append(u[1])
    # TODO just np.array these?

ngs = np.array(ngs)[:, :, 0]
possibilities = np.array(possibilities).transpose()
possibilities_normed = possibilities / np.sum(possibilities, axis=0)

# ngs = np.empty(unload[0][0].shape)
# possibilities = np.empty((len(unload[0][1]), 1))

# for u in unload:
#     ngs = np.hstack([ngs, np.array(u[0])])
#     possibilities = np.hstack(
#         [possibilities, np.array(u[1], ndmin=2).transpose()])

brain = Brain.Brain(len(possibilities_normed))
brain.initWeightsAndBiases(ngs[0])

best = brain.learnRaw(ngs, possibilities_normed, iterations=100000)
fileHelper.fileDumpBaseWeights(best)
close = True
