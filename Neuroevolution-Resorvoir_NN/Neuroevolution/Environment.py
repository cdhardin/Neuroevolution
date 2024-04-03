print('Imported environ')

import numpy as np
from InitializationVariables import *
from scipy.ndimage import distance_transform_bf



#Environment
def initialize():
    environment = np.full((environment_xSize, environment_ySize, 3), 255)
    environment_pop_density = np.zeros((environment_xSize, environment_ySize))
    environment_pheramones = np.zeros((environment_xSize, environment_ySize))
    agents = []
    return environment, agents, environment_pop_density, environment_pheramones

def getBarrierMask():
    barrierMask = np.zeros((environment_xSize, environment_ySize))
#     Small Block center low : 
    barrierMask[1 * environment_xSize//5 : 2 * environment_xSize//5, environment_ySize//3 : 2 * environment_ySize//3]= 1
    barrierMask[environment_ySize//3 : 2 * environment_ySize//3, 1 * environment_xSize//5 : 2 * environment_xSize//5]= 1
    
    return barrierMask

def getBarrierMaskDist(barrierMask):
    distance_transform = distance_transform_bf(barrierMask)
    return distance_transform

def getSurvivalMask():
    survivalMask = np.zeros((environment_xSize, environment_ySize))
#     survivalMask[:, 3 * environment_ySize//4 : ]= 1
    survivalMask[: 1 * environment_ySize//3, : 1 * environment_ySize//3 ]= 1
#     survivalMask[: 1 * environment_ySize//4:, 3 * environment_ySize//4 : ]= 1
#     survivalMask[ 3 * environment_ySize//4:, :1 * environment_ySize//4 ]= 1
#     survivalMask[ 3 * environment_ySize//4:, 3 * environment_ySize//4 : ]= 1

#     survivalMask[ 1 * environment_ySize//4: 3 * environment_ySize//4, 1 * environment_ySize//4: 3 * environment_ySize//4 ]= 1

    

    return survivalMask

def getEmptyBarrierMask():
    barrierMask = np.zeros((environment_xSize, environment_ySize))
    return barrierMask

    
def resetEnv(environment):
    environment = np.full((environment_xSize, environment_ySize, 3), 255)
    return environment

def getPopDensity(environment_pop_density, agents):
    environment_pop_density = np.zeros((environment_xSize, environment_ySize))
    for agent in agents:
        x = agent.xCoord
        y = agent.yCoord
        environment_pop_density[x, y] = environment_pop_density[x, y] + 1  # Note: (y, x) to match NumPy array indexing
    return environment_pop_density

def getPheramones(environment_pheramones, agents):
    environment_pheramones = environment_pheramones * pheramoneDecayRate
    for agent in agents:
        x = agent.xCoord
        y = agent.yCoord
        environment_pheramones[x, y] = environment_pheramones[x, y] + 1  # Note: (y, x) to match NumPy array indexing
    return environment_pheramones

    
