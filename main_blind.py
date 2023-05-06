import GameManagerModule
import BlindClientMapper

# Grid dimensions
GRID_DIM_X = 10
GRID_DIM_Y = 10

# Number of initial tanks
NUM_TANKS = 10

manager = GameManagerModule.GameManager(GRID_DIM_X, GRID_DIM_Y, NUM_TANKS)
mapper = BlindClientMapper.BlindMapper(manager)

a = 1