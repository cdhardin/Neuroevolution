import random

print('imported Agent module')
from NeuralNetwork import * 
from InitializationVariables import *
from Environment import *

class Agent: 
    id = 0
    gene = 0
    agentBrain = 0
    facing = 0   #0 East, 1 North, 2 West, 3 South
    xCoord = 0
    yCoord = 0
    color = 0
    dead = False
    
   
    
    def __init__(self, id, gene, xCoord, yCoord):
        self.id = id
        self.gene = gene
        self.agentBrain = NeuralNetwork(gene)
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.color = getColor(self.agentBrain)
        
    def canMove(self, movement, agents, xWrapping, yWrapping, barrierMask):
        
        canMoveVar = 1

        target_xCoord = self.xCoord + movement[0]
        target_yCoord = self.yCoord + movement[1]
        
        moveFacing = [0, 0, 0]
        if self.facing == 0  : moveFacing[0] = 1
        elif self.facing == 1: moveFacing[1] = 1
        elif self.facing == 2: moveFacing[0] = -1
        elif self.facing == 3: moveFacing[1] = -1
            
        target_xCoord_kill = self.xCoord + movement[0] + moveFacing[0]
        target_yCoord_kill = self.yCoord + movement[1] + moveFacing[1]
            
            

        #Out of bounds:
        if (not xWrapping) and (not target_xCoord < environment_xSize) : canMoveVar = 0
        if (not yWrapping) and (not target_yCoord < environment_ySize) : canMoveVar = 0
        if (not xWrapping) and (not target_xCoord >= 0) : canMoveVar = 0
        if (not yWrapping) and (not target_yCoord >= 0) : canMoveVar = 0
            
        if not canMoveVar : return 0, None, None, None
            
        target_xCoord = target_xCoord % environment_xSize
        target_yCoord = target_yCoord % environment_ySize
        
        target_xCoord_kill = target_xCoord_kill % environment_xSize
        target_yCoord_kill = target_yCoord_kill % environment_ySize
        
        #Barrier Collisions
        
        if barrierMask[target_xCoord, target_yCoord] : canMoveVar = 0
            
        
            
        agent_to_kill = None

        #Only 1 agent per square
        for agent in agents:
            if not agent.dead:
                if agent.xCoord == target_xCoord and agent.yCoord == target_yCoord : canMoveVar = 0
                if agent.xCoord == target_xCoord_kill and agent.yCoord == target_yCoord_kill : agent_to_kill = agent
            
            

        return canMoveVar, target_xCoord, target_yCoord, agent_to_kill
    
    def operate(self, agents, barrierMask,distToBarrier, environment_pop_density, environment_pheramones, killing):
        movement, killForward = self.agentBrain.think(self.facing, self.xCoord, self.yCoord, environment_pop_density, environment_pheramones,barrierMask,distToBarrier, killing)
        canMoveVar, target_xCoord, target_yCoord, agent_to_kill = self.canMove(movement, agents, xWrapping, yWrapping, barrierMask)
        
        if canMoveVar :
            self.xCoord = target_xCoord
            self.yCoord = target_yCoord
            
        if killForward:
            if agent_to_kill : agent_to_kill.die()
        
        self.facing = (self.facing + movement[2]) % 4
    
    def die(self):
        self.dead = True
        self.color = (145, 103, 103)

    
    
        
    
    

def operateAll(agents, barrierMask, distToBarrier, environment_pop_density, environment_pheramones, killing):
    for agent in agents:
        if not agent.dead:
            agent.operate(agents, barrierMask,distToBarrier, environment_pop_density, environment_pheramones, killing)
        
def getColor(agentBrain):
    #R - kill
    #G - move EW
    #B - move NS
    R = 0
    G = 0
    B = 0
    for edge in agentBrain.network:
        edgeStrength = edge[2]
        edgeTarget = edge[1]
        if   edgeTarget == 0  : None
        elif edgeTarget == 1  : B += edgeStrength
        elif edgeTarget == 2  : G += edgeStrength
        elif edgeTarget == 3  :
            B += edgeStrength
            G += edgeStrength
        elif edgeTarget == 4  : B -= edgeStrength
        elif edgeTarget == 5  : G -= edgeStrength
        elif edgeTarget == 6  :
            B -= edgeStrength
            G -= edgeStrength
        elif edgeTarget == 7  :
            B -= edgeStrength
            G += edgeStrength                
        elif edgeTarget == 8  :
            B += edgeStrength
            G -= edgeStrength
        elif edgeTarget == 9  : None
        elif edgeTarget == 10 : None
        elif edgeTarget == 11 : None  
        elif edgeTarget == 12 : None
        elif edgeTarget == 13 : R += edgeStrength

    maxColor = 50 * network_edges
    return (R,G,B)
    

