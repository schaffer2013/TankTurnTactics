STRATEGY_NO_RESTRICTIONS = 0
STRATEGY_NO_MOVE = 1
STRATEGY_NO_DONATE = 2


def getMask(strategyInt, lenValidActions):
    # PASS_CMD = 0
    # MOVE_RIGHT_CMD = 1
    # MOVE_LEFT_CMD = 2
    # MOVE_UP_CMD = 3
    # MOVE_DOWN_CMD = 4
    # INCREASE_RANGE_CMD = 5
    # then SHOOT = (5 + i * 2)
    # and DONATE TO = (5 + i * 2 + 1)
    # total bits = 6 + (2n)
    if (strategyInt == STRATEGY_NO_RESTRICTIONS):
        return [True] * (lenValidActions)
    if (strategyInt == STRATEGY_NO_MOVE):
        allowed = []
        allowed.append(True)  # PASS
        allowed.extend([False] * 4)  # Moves
        allowed.append(True)  # Increase range
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
        allowShoot = True
        allowDonate = False
        allowed.extend([allowShoot, allowDonate] *
                       int((lenValidActions - 6)/2))
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
