
import numpy as np
import random 
from InitializationVariables import *

def activationThreshold(inputValue):
    probability = np.arctan(inputValue / 100) * 2 / np.pi
    roll = random.random()
    return roll > probability

    

    
##Action Functions: Input value from a single source range [-100, 100], sum all sources 
def function0(fire):
    if fire : return [0,0,0]
    return [0,0,0]

def function1(fire):
    if fire : return [0,1,0]
    return [0,0,0]

def function2(fire):
    if fire : return [1,0,0]
    return [0,0,0]

def function3(fire):
    if fire : return [1,1,0]
    return [0,0,0]

def function4(fire):
    if fire : return [0,-1,0]
    return [0,0,0]

def function5(fire):
    if fire : return [-1,0,0]
    return [0,0,0]

def function6(fire):
    if fire : return [-1,-1,0]
    return [0,0,0]

def function7(fire):
    if fire : return [1,-1,0]
    return [0,0,0]

def function8(fire):
    if fire : return [-1,1,0]
    return [0,0,0]


def function9(fire, facing):     #Move Forward
    moveTo = [0, 0, 0]
    if facing == 0  : moveTo[0] = 1
    elif facing == 1: moveTo[1] = 1
    elif facing == 2: moveTo[0] = -1
    elif facing == 3: moveTo[1] = -1
    
    if fire : return moveTo
    return [0,0,0]

def function10(fire, facing):    #Move Backward
    moveTo = [0, 0, 0]
    if facing == 0  : moveTo[0] = -1
    elif facing == 1: moveTo[1] = -1
    elif facing == 2: moveTo[0] = 1
    elif facing == 3: moveTo[1] = 1
    
    if fire : return moveTo
    return [0,0,0]

def function11(fire, facing):    #Turn counterClockwise
    if fire : return [0,0,1]
    return [0,0,0]

def function12(fire, facing):    #Turn Clockwise
    if fire : return [0,0,-1]
    return [0,0,0]

def functionKill(fire, killing):
    if killing: 
        if random.random() > .9: return fire
    return False



    





##Sensor Functions:
def getLoc_X(xCoord):
    xPercent = xCoord / environment_xSize
    return xPercent * 100

def getLoc_Y(yCoord):
    yPercent = yCoord / environment_ySize
    return yPercent * 100

def getBoundary_Dist_x(xCoord):
    xPercent = (environment_xSize - xCoord) / environment_xSize
    return xPercent * 100

def getBoundary_Dist_y(yCoord):
    yPercent = (environment_ySize - yCoord) / environment_ySize
    return yPercent * 100

def getBoundary_Dist(xCoord, yCoord):
    minDist = min(getBoundary_Dist_x(xCoord), getBoundary_Dist_y(yCoord), getLoc_X(xCoord), getLoc_Y(yCoord))
    return minDist

def getGenetic_similarity_forward(facing):
    return 50

def getLast_Move_X(lastMove):
    return lastMove[0] * 50

def getLast_Move_Y(lastMove):
    return lastMove[1] * 50

def getPopulationForward(environment_pop_density, facing, xCoord, yCoord):
    xTarget = xCoord
    yTarget = yCoord
    if facing == 0   : xTarget = (xCoord + 1)%len(environment_pop_density)
    elif facing == 1 : yTarget = (yCoord + 1)%len(environment_pop_density[0])
    elif facing == 2 : xTarget = (xCoord - 1)%len(environment_pop_density)
    elif facing == 3 : yTarget = (yCoord - 1)%len(environment_pop_density[0])
    return environment_pop_density[xTarget][yTarget] * popScale

def getBarrierForward(barrierMask, facing, xCoord, yCoord):
    xTarget = xCoord
    yTarget = yCoord
    if facing == 0   : xTarget = (xCoord + 1)%len(barrierMask)
    elif facing == 1 : yTarget = (yCoord + 1)%len(barrierMask[0])
    elif facing == 2 : xTarget = (xCoord - 1)%len(barrierMask)
    elif facing == 3 : yTarget = (yCoord - 1)%len(barrierMask[0])
    return barrierMask[xTarget][yTarget] * 100
    

def getPopulationDensity(environment_pop_density, xCoord, yCoord):
    sumQueenArea = 0
    for xChange in [-1, 0, 1]:
        for yChange in [-1, 0 , 1]:
            xTarget = (xCoord + xChange)%len(environment_pop_density)
            yTarget = (yCoord + yChange)%len(environment_pop_density[0])
            sumQueenArea = sumQueenArea + environment_pop_density[xTarget][yTarget]
    return sumQueenArea * popScale

def getPopulationGradient_xDirection(environment_pop_density, xCoord, yCoord):
    xTarget_behind = (xCoord - 1)%len(environment_pop_density)
    xTarget_front  = (xCoord + 1)%len(environment_pop_density)
    gradient = (environment_pop_density[xTarget_front][yCoord] - environment_pop_density[xTarget_behind][yCoord])/2
    return popScale * gradient

def getPopulationGradient_yDirection(environment_pop_density, xCoord, yCoord):
    yTarget_behind = (yCoord - 1)%len(environment_pop_density[0])
    yTarget_front  = (yCoord + 1)%len(environment_pop_density[0])
    gradient = (environment_pop_density[xCoord][yTarget_front] - environment_pop_density[xCoord][yTarget_behind])/2
    return popScale * gradient

def getOscilatorVal(age):
    freq = 4
    oscilationVal = np.sin(2*np.pi * freq * age / steps_per_cycle)
    return oscilationVal*100

def getAge(age):
    agePercent = age / steps_per_cycle
    return agePercent * 200

def getYouth(age):
    agePercent = age / steps_per_cycle
    return (1 - agePercent) * 200

def getBoundaryDistForward(facing, xCoord, yCoord):
    if   facing == 0 : return getBoundary_Dist_x(xCoord)
    elif facing == 1 : return getBoundary_Dist_y(yCoord)
    elif facing == 2 : return getLoc_X(xCoord)
    elif facing == 3 : return getLoc_Y(yCoord)
    return 0

def getFacingX(facing):
    if   facing == 0 : return 100
    elif facing == 2 : return -100
    else : return 0

def getFacingY(facing):
    if   facing == 1 : return 100
    elif facing == 3 : return -100
    else : return 0

def getRandom():
    return random.randint(0,100)

def getPheramones(environment_pheramones, xCoord, yCoord):
    return environment_pheramones[xCoord][yCoord] * pheramoneScale

def getPheramonesForward(environment_pheramones, facing, xCoord, yCoord):
    xTarget = xCoord
    yTarget = yCoord
    if facing == 0   : xTarget = (xCoord + 1)%len(environment_pheramones)
    elif facing == 1 : yTarget = (xCoord + 1)%len(environment_pheramones)
    elif facing == 2 : xTarget = (xCoord - 1)%len(environment_pheramones[0])
    elif facing == 3 : yTarget = (xCoord - 1)%len(environment_pheramones[0])
    return environment_pheramones[xTarget][yTarget] * pheramoneScale
    
def getBarrierClosest(xCoord, yCoord, distToBarrier):
    return 100 * distToBarrier[xCoord][yCoord] / environment_xSize
    
###Finish Functions

