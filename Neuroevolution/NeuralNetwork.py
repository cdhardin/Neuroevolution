print('imported Neural Network module')
import numpy as np
import random 
from InitializationVariables import *
from NodeFunctions import *

activationNodeCount = 14
sensorNodeCount = 22                       

def unravelDNA(gene):
    strand = []
    for i in range(3):
        strand.append(gene % 100)
        gene = (gene - gene % 100)/100
    return strand, gene

def getEdge(gene):
    strand, gene = unravelDNA(gene)
    edge = [0, 0, 0] #Start sensor, end action, strength
    edge[0] = strand[0] % sensorNodeCount
    edge[1] = strand[1] % activationNodeCount
    edge[2] = strand[2] 
    return edge, gene

def getNetwork(gene):
    edges = []
    while gene > 99999 :       #Minimum 6 digits left
        edge, gene = getEdge(gene)
        edges.append(edge)
    return edges
    
def addMoves(move1, move2):
    move = [0, 0, 0]
    move[0] = move1[0] + move2[0]
    move[1] = move1[1] + move2[1]
    move[2] = move1[2] + move2[2]
    return move

def combine(senseStrength, edgeStrength):
    return senseStrength * edgeStrength / 50


    
    
class NeuralNetwork:
    gene = 0
    network = []
    sensorVals = []
    facing = 0
    age = 0
    lastMove = [0, 0 ,0]
    
    def think(self, facing, xCoord, yCoord, environment_pop_density, environment_pheramones, barrierMask, distToBarrier, killing):
        self.sense(facing, xCoord, yCoord, environment_pop_density, environment_pheramones, barrierMask, distToBarrier)
        movement, killForward = self.activate(killing)
        self.facing = movement[2]
        self.lastMove = movement
        return movement, killForward
    
    def sense(self, facing, xCoord, yCoord, environment_pop_density, environment_pheramones, barrierMask, distToBarrier): 
        self.age = self.age + 1
        sensorVals = [
            getLoc_X(xCoord),
            getLoc_Y(yCoord),
            getBoundary_Dist_x(xCoord),
            getBoundary_Dist(xCoord, yCoord),
            getBoundary_Dist_y(yCoord),
#             getGenetic_similarity_forward(facing),
            getYouth(self.age),
            getLast_Move_X(self.lastMove),
            getLast_Move_Y(self.lastMove),
            getPopulationForward(environment_pop_density, facing, xCoord, yCoord),
            getBoundaryDistForward(facing, xCoord, yCoord),
            getPopulationDensity(environment_pop_density, xCoord, yCoord),
            getPopulationGradient_xDirection(environment_pop_density, xCoord, yCoord),
            getPopulationGradient_yDirection(environment_pop_density, xCoord, yCoord),
            getOscilatorVal(self.age),
            getAge(self.age),
            getBarrierForward(barrierMask, facing, xCoord, yCoord),
            getFacingX(facing),
            getFacingY(facing),
            getRandom(),
            getPheramones(environment_pheramones, xCoord, yCoord),
            getPheramonesForward(environment_pheramones, facing, xCoord, yCoord),
            getBarrierClosest(xCoord, yCoord, distToBarrier)
        ]
        self.sensorVals = sensorVals


        
        
    def activate(self, killing):
        movement = [0, 0, 0]
        actionValues = np.zeros(activationNodeCount)
        for edge in self.network:
            senseStrength = self.sensorVals[int(edge[0])]
            edgeStrength = edge[2]
            
            if   edge[1] == 0  : actionValues[0] = actionValues[0] + combine(senseStrength, edgeStrength)
            elif edge[1] == 1  : actionValues[1] = actionValues[1] + combine(senseStrength, edgeStrength)
            elif edge[1] == 2  : actionValues[2] = actionValues[2] + combine(senseStrength, edgeStrength)
            elif edge[1] == 3  : actionValues[3] = actionValues[3] + combine(senseStrength, edgeStrength)
            elif edge[1] == 4  : actionValues[4] = actionValues[4] + combine(senseStrength, edgeStrength)
            elif edge[1] == 5  : actionValues[5] = actionValues[5] + combine(senseStrength, edgeStrength)
            elif edge[1] == 6  : actionValues[6] = actionValues[6] + combine(senseStrength, edgeStrength)
            elif edge[1] == 7  : actionValues[7] = actionValues[7] + combine(senseStrength, edgeStrength)
            elif edge[1] == 8  : actionValues[8] = actionValues[8] + combine(senseStrength, edgeStrength)
            elif edge[1] == 9  : actionValues[9] = actionValues[9] + combine(senseStrength, edgeStrength)
            elif edge[1] == 10 : actionValues[10] = actionValues[10] + combine(senseStrength, edgeStrength)
            elif edge[1] == 11 : actionValues[11] = actionValues[11] + combine(senseStrength, edgeStrength)
            elif edge[1] == 12 : actionValues[12] = actionValues[12] + combine(senseStrength, edgeStrength)
            elif edge[1] == 13 : actionValues[13] = actionValues[13] + combine(senseStrength, edgeStrength)
            else : None
#                 print(edge[1])
#                 print('ERROR')


        
        movement = addMoves(movement, function0(actionValues[0])) 
        movement = addMoves(movement, function1(actionValues[1])) 
        movement = addMoves(movement, function2(actionValues[2])) 
        movement = addMoves(movement, function3(actionValues[3])) 
        movement = addMoves(movement, function4(actionValues[4])) 
        movement = addMoves(movement, function5(actionValues[5])) 
        movement = addMoves(movement, function6(actionValues[6])) 
        movement = addMoves(movement, function7(actionValues[7])) 
        movement = addMoves(movement, function8(actionValues[8])) 
        movement = addMoves(movement, function9(actionValues[9], self.facing)) 
        movement = addMoves(movement, function10(actionValues[10], self.facing)) 
        movement = addMoves(movement, function11(actionValues[11], self.facing)) 
        movement = addMoves(movement, function12(actionValues[12], self.facing)) 
        killForward = functionKill(actionValues[13], killing)
        
        
                
        return movement, killForward
            
            
    
    
    
    def __init__(self, gene):
        self.gene = gene
        self.network = getNetwork(gene)
        
    
    
