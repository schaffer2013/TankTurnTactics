import Brain
import FileHelper
import numpy as np

NUM_TANKS = 10
DIM = 15

fileHelper = FileHelper.FileHelper(NUM_TANKS, DIM, Brain.LAYER_1_NODES)

unload = (fileHelper.undumpPossibilities())
total = 0
for x in unload:
    for y in x:
        for z in y:
            if type(z) == np.ndarray:
                if len (z) > 1:
                    a =1
            total += 1
        print(f'X: {len(x)} Y: {len(y)}')
close = True
