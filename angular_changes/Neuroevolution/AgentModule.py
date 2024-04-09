import random

print('imported Agent module')
from NeuralNetwork import * 
from InitializationVariables import *
from Environment import *

class Agent: 
    id = 0
    gene = []
    agentBrain = 0
    
    angle = 0   #0 East, 1 North, 2 West, 3 South
    angularVelocity = 0
    forwardVelocity = 0

    
    xCoord = 0
    yCoord = 0
    color = 0
    dead = False
    
   
    
    def __init__(self, id, gene, xCoord, yCoord):
        self.id = id
        self.gene = gene
        self.agentBrain = NeuralNetwork(gene)
        self.color = getColor(self.agentBrain)

        self.xCoord = xCoord
        self.yCoord = yCoord

        self.angularVelocity = 0
        self.angle = 0

        self.forwardVelocity = 0
        
        
        
    def canMove(self, movement, agents, xWrapping, yWrapping, barrierMask):
        
        canMoveVar = 1

        target_xCoord = self.xCoord + movement[0]
        target_yCoord = self.yCoord + movement[1]

            
        target_xCoord_kill = self.xCoord + movement[0] 
        target_yCoord_kill = self.yCoord + movement[1] 
            

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
                if agent == self:
                    continue

                ##Collision with other agent
                if abs(agent.xCoord - target_xCoord) < 2*agent_radius +1 :
                    if abs(agent.yCoord - target_yCoord) < 2*agent_radius +1 :               
                        canMoveVar = 0

                        ##IF collision kills both
                        if collisionKillsBoth : 
                            agent.die()

                ##Kill other agent
                if abs(agent.xCoord - target_xCoord_kill) < 2*agent_radius +1 :
                    if abs(agent.yCoord - target_yCoord_kill) < 2*agent_radius +1 :               
                        agent_to_kill = agent
            

        return canMoveVar, target_xCoord, target_yCoord, agent_to_kill
    
    def operate(self, agents, barrierMask,distToBarrier, environment_pop_density, killing, survivalMask):
        movement, killForward, plotpoints = self.agentBrain.think(self.angle, self.angularVelocity,self.xCoord, self.yCoord, barrierMask, killing, environment_pop_density, survivalMask)

        ## movement = [ change Angle, change Angle velocity, change velocity]
        

        self.forwardVelocity = self.forwardVelocity + movement[2]

        if self.forwardVelocity > maxVelocity : self.forwardVelocity = maxVelocity
        if self.forwardVelocity < -maxVelocity : self.forwardVelocity = -maxVelocity
        
        self.angularVelocity = self.angularVelocity + movement[1]/10

        if self.angularVelocity > maxAngularVelocity : self.angularVelocity = maxAngularVelocity
        if self.angularVelocity < -maxAngularVelocity : self.angularVelocity = -maxAngularVelocity

        
        
        self.angle = (self.angle +  movement[0]/20 + self.angularVelocity ) % (2*np.pi)
        
        
        dx = np.cos(self.angle)
        dy = np.sin(self.angle)

        change_x = round(dx * self.forwardVelocity)
        change_y = round(dy * self.forwardVelocity)
        
        changeLocations = [change_x, change_y] # dx, dy
        
        canMoveVar, target_xCoord, target_yCoord, agent_to_kill = self.canMove(changeLocations, agents, xWrapping, yWrapping, barrierMask)

        
        if canMoveVar :
            self.xCoord = target_xCoord
            self.yCoord = target_yCoord
            
        if  collisionsKill and not canMoveVar:
            self.die()
            # self.color = (.8,.2,.6)
            
            
        if killForward:
            if agent_to_kill : agent_to_kill.die()
        
        self.angle = (self.angle +  movement[2] / 2) % (2*np.pi)

        return plotpoints
    
    def die(self):
        self.dead = True
        self.color = (.8,.2,.6)

    
    
        
    
    

def operateAll(agents, barrierMask, distToBarrier, environment_pop_density, killing, survivalMask):
    plotpoints = []
    for agent in agents:
        if not agent.dead:
            pts = agent.operate(agents, barrierMask,distToBarrier, environment_pop_density, killing, survivalMask)
            plotpoints = plotpoints + pts
    return plotpoints
        
def getColor(agentBrain):
    # #R - kill
    # #G - move EW
    # #B - move NS
    # R = 0
    # G = 0
    # B = 0
    # for edge in agentBrain.network:
    #     edgeStrength = edge[2]
    #     edgeTarget = edge[1]
    #     if   edgeTarget == 0  : None
    #     elif edgeTarget == 1  : B += edgeStrength
    #     elif edgeTarget == 2  : G += edgeStrength
    #     elif edgeTarget == 3  :
    #         B += edgeStrength
    #         G += edgeStrength
    #     elif edgeTarget == 4  : B -= edgeStrength
    #     elif edgeTarget == 5  : G -= edgeStrength
    #     elif edgeTarget == 6  :
    #         B -= edgeStrength
    #         G -= edgeStrength
    #     elif edgeTarget == 7  :
    #         B -= edgeStrength
    #         G += edgeStrength                
    #     elif edgeTarget == 8  :
    #         B += edgeStrength
    #         G -= edgeStrength
    #     elif edgeTarget == 9  : None
    #     elif edgeTarget == 10 : None
    #     elif edgeTarget == 11 : None  
    #     elif edgeTarget == 12 : None
    #     elif edgeTarget == 13 : R += edgeStrength

    # maxColor = 50 * network_edges
    return (.2,.2,.2)
    

