print('Imported environ')

import numpy as np
from InitializationVariables import *
from scipy.ndimage import distance_transform_bf



#Environment
def initialize():
    environment = np.full((environment_xSize, environment_ySize, 3), 255)
    environment_pop_density = np.full((environment_xSize, environment_ySize), False)
    agents = []
    return environment, agents, environment_pop_density

def getBarrierMask():
    barrierMask = np.full((environment_xSize, environment_ySize), False)
#     Small Block center low : 
    barrierMask[1 * environment_xSize//5 : 2 * environment_xSize//5, environment_ySize//3 : 2 * environment_ySize//3]= True
    barrierMask[environment_ySize//3 : 2 * environment_ySize//3, 1 * environment_xSize//5 : 2 * environment_xSize//5]= True
    
    return barrierMask

def getBarrierMaskDist(barrierMask):
    distance_transform = distance_transform_bf(barrierMask)
    return distance_transform

def getSurvivalMask():
    survivalMask = np.full((environment_xSize, environment_ySize), False)
#     survivalMask[:, 3 * environment_ySize//4 : ]= 1
    survivalMask[: 1 * environment_ySize//3, : 1 * environment_ySize//3 ]= True
#     survivalMask[: 1 * environment_ySize//4:, 3 * environment_ySize//4 : ]= 1
#     survivalMask[ 3 * environment_ySize//4:, :1 * environment_ySize//4 ]= 1
#     survivalMask[ 3 * environment_ySize//4:, 3 * environment_ySize//4 : ]= 1

#     survivalMask[ 1 * environment_ySize//4: 3 * environment_ySize//4, 1 * environment_ySize//4: 3 * environment_ySize//4 ]= 1

    

    return survivalMask

def getEmptyBarrierMask():
    barrierMask = np.full((environment_xSize, environment_ySize), False)
    return barrierMask

    
def resetEnv(environment):
    environment = np.full((environment_xSize, environment_ySize, 3), 255)
    return environment

def getPopDensity(environment_pop_density, agents):
    
    environment_pop_density = np.full((environment_xSize, environment_ySize), False)
    
    for agent in agents:
        x = agent.xCoord
        y = agent.yCoord

        giveWidth = range(-agent_radius,agent_radius+1)
        for x_ in giveWidth:
                for y_ in giveWidth:
                    at_x = (x+x_)%environment_xSize
                    at_y = (y+y_)%environment_ySize
                    
                    environment_pop_density[at_x, at_y] = True
                    
    return environment_pop_density



    
