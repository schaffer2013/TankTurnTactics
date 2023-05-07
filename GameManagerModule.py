from Tank import Tank
import random
import jsonpickle


class GameManager:
    def __init__(self, DIM_X, DIM_Y, numOfTanks):
        self.isAWin = False
        self.numTanks = numOfTanks
        self.AllTanks = []

        # Add tanks
        for i in range(numOfTanks):
            overlap = True
            while (overlap):
                overlap = False
                x = random.randint(0, DIM_X - 1)
                y = random.randint(0, DIM_Y - 1)
                for t in self.AllTanks:
                    if (t.x == x and t.y == y):
                        overlap = True
                        break
                if (not overlap):
                    self.AllTanks.append(Tank(len(self.AllTanks), x, y))

        self.setActiveTankIndex(-1)
        self.increaseActiveTankIndex()

        self.dimX = DIM_X
        self.dimY = DIM_Y

    def getAllTanks(self):
        return self.AllTanks

    def getAliveTanks(self):
        aliveTanks = []
        for t in self.AllTanks:
            if t.isAlive:
                aliveTanks.append(t)
        return aliveTanks

    def getActiveTank(self):
        return self.getAllTanks()[self.activeTankIndex]

    def getInactiveTanksCopy(self):
        c = self.getAllTanks().copy()
        del c[self.activeTankIndex]
        return c

    def getInactiveAliveTanksCopy(self):
        c = self.getAllTanks().copy()
        del c[self.activeTankIndex]
        newArray = []
        for t in c:
            if t.isAlive:
                newArray.append(t)
        return newArray

    def setActiveTankIndex(self, newIndex):
        self.activeTankIndex = newIndex
        self.setActiveTank()

    def increaseActiveTankIndex(self):
        tempIndex = self.activeTankIndex + 1
        self.setActiveTankIndex(tempIndex % len(self.getAllTanks()))
        if self.isAWin:
            return
        active = self.getActiveTank()
        if (active.isAlive):
            self.increaseActiveTankActionPoints()
        else:
            self.increaseActiveTankIndex()

    def increaseTankActionPoints(self, target):
        target.actionPoints += 1

    def increaseActiveTankActionPoints(self):
        self.getActiveTank().actionPoints += 1

    def decreaseActiveTankActionPoints(self):
        self.getActiveTank().actionPoints -= 1
        if self.getActiveTank().actionPoints <= 0:
            self.increaseActiveTankIndex()

    def setActiveTank(self):
        for t in self.getAllTanks():
            t.isActive = False
        self.getActiveTank().isActive = True

    def getActiveTankHasActionPoints(self):
        return self.getActiveTank().actionPoints > 0

    def getShootableSpots(self):
        t = self.getActiveTank()
        shootableSpots = []
        for c in range(self.dimX):
            for r in range(self.dimY):
                dist = self.boxDistance((c, r), (t.x, t.y))
                if (dist > 0 and dist <= t.range):
                    shootableSpots.append((c, r))
        return shootableSpots

    def canMoveActiveTank(self, deltaX, deltaY):
        t = self.getActiveTank()
        tempNewX = t.x + deltaX
        tempNewY = t.y + deltaY
        if (tempNewX >= self.dimX or tempNewX < 0):
            return False
        if (tempNewY >= self.dimY or tempNewY < 0):
            return False

        inactives = self.getInactiveAliveTanksCopy()
        for i in inactives:
            if (i.x == tempNewX and i.y == tempNewY):
                return False
        return True

    def moveActiveTank(self, deltaX, deltaY):
        activeTank = self.getActiveTank()
        activeTank.x += deltaX
        activeTank.y += deltaY
        self.decreaseActiveTankActionPoints()

    def tryMoveActiveTankRight(self):
        return self.tryMoveActiveTank(1, 0)

    def tryMoveActiveTankLeft(self):
        return self.tryMoveActiveTank(-1, 0)

    def tryMoveActiveTankUp(self):
        return self.tryMoveActiveTank(0, -1)

    def tryMoveActiveTankDown(self):
        return self.tryMoveActiveTank(0, 1)

    def tryMoveActiveTank(self, deltaX, deltaY):
        if self.canMoveActiveTank(deltaX, deltaY):
            self.moveActiveTank(deltaX, deltaY)
            return True
        return False

    def tryShootXY(self, xy):
        for target in self.getInactiveTanksCopy():
            if (target.x == xy[0] and target.y == xy[1]):
                return self.tryShootOrDonate(target.index, True)
        return False

    def tryShootOrDonate(self, targetIndex, isShoot):
        success = self.canShootOrDonate(targetIndex)
        if success:
            target = self.getAllTanks()[targetIndex]
            if isShoot:
                self.shoot(target)
            else:
                self.donateTo(target)
        return success

    def canShootOrDonate(self, targetIndex):
        success = False
        activeTank = self.getActiveTank()
        if (not self.getActiveTankHasActionPoints()):
            return False
        target = self.getAllTanks()[targetIndex]
        dist = self.boxDistance((target.x, target.y),
                                (activeTank.x, activeTank.y))
        if (dist > 0 and dist <= activeTank.range and target.isAlive):
            success = True
        return success

    def shoot(self, target):
        if (target.extra_lives == 0):
            target.isAlive = False
            if (len(self.getAliveTanks()) <= 1):
                self.isAWin = True
        else:
            target.extra_lives -= 1
        self.decreaseActiveTankActionPoints()

    def donateTo(self, target):
        self.increaseTankActionPoints(target)
        self.decreaseActiveTankActionPoints()

    def increaseActiveTankRange(self):
        self.getActiveTank().range += 1
        self.decreaseActiveTankActionPoints()

    def manhattanDistance(self, xy1, xy2):
        return abs(xy1[0]-xy2[0]) + abs(xy1[1]-xy2[1])

    def boxDistance(self, xy1, xy2):
        return max(abs(xy1[0]-xy2[0]), abs(xy1[1]-xy2[1]))

    def getFullGameStatus(self):
        jsonStr = jsonpickle.encode(self)
        return (jsonStr)
