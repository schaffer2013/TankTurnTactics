import numpy as np

STRATEGY_NO_RESTRICTIONS = 0
STRATEGY_NO_MOVE = 1
STRATEGY_NO_DONATE = 2
STRATEGY_NO_INCREASE_RANGE = 4
STRATEGY_NO_WITHER = 8
STRATEGY_SIT_AND_SHOOT_ON_SIGHT = 15


def getMask(strategyInt, lenValidActions):
    # PASS_CMD = 0
    # MOVE_RIGHT_CMD = 1
    # MOVE_LEFT_CMD = 2
    # MOVE_UP_CMD = 3
    # MOVE_DOWN_CMD = 4
    # INCREASE_RANGE_CMD = 5
    # WITHER_CMD = 6
    # then SHOOT = (6 + i * 2)
    # and DONATE TO = (6 + i * 2 + 1)
    # total bits = 7 + (2n)
    if (strategyInt == STRATEGY_NO_RESTRICTIONS):
        return [True] * (lenValidActions)
    if (strategyInt == STRATEGY_NO_MOVE):
        allowed = []
        allowed.append(True)  # PASS
        allowed.extend([False] * 4)  # Moves
        allowed.append(True)  # Increase range
        allowed.append(True)  # Wither
        allowShoot = True
        allowDonate = True
        allowed.extend([allowShoot, allowDonate] *
                       int((lenValidActions - 6)/2))
        return allowed
    if (strategyInt == STRATEGY_NO_DONATE):
        allowed = []
        allowed.append(True)  # PASS
        allowed.extend([True] * 4)  # Moves
        allowed.append(True)  # Increase range
        allowed.append(True)  # Wither
        allowShoot = True
        allowDonate = False
        allowed.extend([allowShoot, allowDonate] *
                       int((lenValidActions - 6)/2))
        return allowed
    if (strategyInt == STRATEGY_NO_INCREASE_RANGE):
        allowed = []
        allowed.append(True)  # PASS
        allowed.extend([True] * 4)  # Moves
        allowed.append(False)  # Increase range
        allowed.append(True)  # Wither
        allowShoot = True
        allowDonate = True
        allowed.extend([allowShoot, allowDonate] *
                       int((lenValidActions - 7)/2))
        return allowed
    if (strategyInt == STRATEGY_NO_WITHER):
        allowed = []
        allowed.append(True)  # PASS
        allowed.extend([True] * 4)  # Moves
        allowed.append(True)  # Increase range
        allowed.append(False)  # Wither
        allowShoot = True
        allowDonate = True
        allowed.extend([allowShoot, allowDonate] *
                       int((lenValidActions - 7)/2))
        return allowed
    if (strategyInt == STRATEGY_SIT_AND_SHOOT_ON_SIGHT):
        noMove_np = np.array(getMask(STRATEGY_NO_MOVE, lenValidActions))
        noDonate_np = np.array(getMask(STRATEGY_NO_DONATE, lenValidActions))
        noIncrease_np = np.array(getMask(STRATEGY_NO_INCREASE_RANGE, lenValidActions))
        noWither_np = np.array(getMask(STRATEGY_NO_WITHER, lenValidActions))
        allowed = list(noMove_np & noDonate_np & noIncrease_np & noWither_np)
        return allowed


def pruneValidActions(validActions, maskEnumOrMaskEnums):
    if (type(maskEnumOrMaskEnums) == list):
        runningMask = validActions
        for m in maskEnumOrMaskEnums:
            runningMask = pruneValidActions(runningMask, m)
        return runningMask
    else:
        runningMask = []
        lenValidActions = len(validActions)
        mask = getMask(maskEnumOrMaskEnums, lenValidActions)
        for i in range(lenValidActions):
            runningMask.append(validActions[i] and mask[i])
        return runningMask


mask1 = getMask(STRATEGY_NO_DONATE, 26)
#mask2 = getMask(STRATEGY_NO_MOVE, len(mask1))
p = pruneValidActions(mask1, STRATEGY_NO_MOVE)
a = 1
