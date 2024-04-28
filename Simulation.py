print('imported Simulation')

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
import math
import time
import networkx as nx


from NeuralNetwork import * 
from Observation import *
from AgentModule import *
from InitializationVariables import *
from Environment import *
from Evolution import initializeAgents, runCycle, simCycle



def RunSim(gene):
    #Initialize environment and next_environment
    environment, agents, environment_pop_density = initialize()
    
    agents = initializeAgents(agent_count, agents, gene)
    
    barrierMask = getBarrierMask()
    distToBarrier = getBarrierMaskDist(barrierMask)
    survivalMask = getSurvivalMask()
    
    starter_agents = agents
    
    
    ###For an easier environment that reaches equilibrium much faster
    
    # barrierMask = getEmptyBarrierMask()
    survivalMask[0:-1,0:-1] = 0
    # # survivalMask[environment_xSize//4 : 3*environment_xSize//4, environment_ySize//4 : 3*environment_ySize//4  ]= 1
    survivalMask[:, 0 :environment_xSize//4   ]= 1
    
    ### easy env end

    livingAgents, environment, killcount = simCycle(steps_per_cycle, agents, environment, barrierMask, distToBarrier, survivalMask,environment_pop_density, killing)

    return len(livingAgents)/agent_count


def WatchSim(gene):
    #Initialize environment and next_environment
    environment, agents, environment_pop_density = initialize()
    
    agents = initializeAgents(agent_count, agents, gene)
    
    barrierMask = getBarrierMask()
    distToBarrier = getBarrierMaskDist(barrierMask)
    survivalMask = getSurvivalMask()
    
    starter_agents = agents
    
    
    ###For an easier environment that reaches equilibrium much faster
    
    barrierMask = getEmptyBarrierMask()
    survivalMask[0:-1,0:-1] = 0
    # survivalMask[environment_xSize//4 : 3*environment_xSize//4, environment_ySize//4 : 3*environment_ySize//4  ]= 1
    survivalMask[:, 0 :environment_xSize//4   ]= 1
    
    ### easy env end

    livingAgents, environment, killcount = runCycle(steps_per_cycle, agents, environment, barrierMask, distToBarrier, survivalMask,environment_pop_density, killing)

    return len(livingAgents)/agent_count
