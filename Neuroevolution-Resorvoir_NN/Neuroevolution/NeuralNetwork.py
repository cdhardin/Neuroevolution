print('imported Neural Network module')
import numpy as np
from numpy.linalg import eigvals

import random 
from InitializationVariables import *
from NodeFunctions import *

activationNodeCount = 14
sensorNodeCount = 22  




def getANetwork(D_r):
    return generate_random_adjacency_matrix(D_r, 4, .8)

def generate_random_adjacency_matrix(N, avg_degree, spectral_radius):
    # Initialize adjacency matrix
    A = np.zeros((N, N))
    
    # Generate random edges to achieve the desired average degree
    num_edges = int(N * avg_degree/2)  # Undirected graph, so divide by 2
    edges = np.random.choice(N, size=(num_edges, 2), replace=True)
    
    # Generate random weights from a normal distribution centered around the spectral radius
    weights = np.random.normal(loc=1, scale=0.3, size=num_edges)
    weights = np.ones(num_edges)

    inhibitorProb = .2
    
    for idx in range(len(weights)):
        if random.random() < inhibitorProb:
            weights[idx] = -1
    
    # Populate the adjacency matrix with the generated edges and weights
    for idx, (i, j) in enumerate(edges):
        if i != j:  # Avoid self-loops
            A[i, j] +=weights[idx]
            A[j, i] +=weights[idx]  # Undirected graph

    current_radius = max(abs(eigvals(A)))
    A *= spectral_radius / current_radius
            
    return A

def addMoves(move1, move2):
    move = [0, 0, 0]
    move[0] = move1[0] + move2[0]
    move[1] = move1[1] + move2[1]
    move[2] = move1[2] + move2[2]
    return move

def getWin(D_r):
    N = sensorNodeCount
    M = D_r
    p = .2
    np.random.seed(41544)
    return np.random.choice([0, 1], size=(N, M), p=[1-p, p])



def shouldFire(arr):
    sigmoid = np.tanh(arr)
    random_array = np.random.rand(*arr.shape)
    fire = random_array<sigmoid
    
    return fire


def getAction(thought, facing):

    fireNodes = shouldFire(thought)
    
    
    movement = [0, 0, 0]

    # print(f' Firing nodes: {fireNodes}')
    
    movement = addMoves(movement, function0(fireNodes[0]))
    movement = addMoves(movement, function1(fireNodes[1]))
    movement = addMoves(movement, function2(fireNodes[2]))
    movement = addMoves(movement, function3(fireNodes[3]))
    movement = addMoves(movement, function4(fireNodes[4]))
    movement = addMoves(movement, function5(fireNodes[5]))
    movement = addMoves(movement, function6(fireNodes[6]))
    movement = addMoves(movement, function7(fireNodes[7]))
    movement = addMoves(movement, function8(fireNodes[8]))
    
    movement = addMoves(movement, function9(fireNodes[9], facing))
    movement = addMoves(movement, function10(fireNodes[10], facing))
    movement = addMoves(movement, function11(fireNodes[11], facing))
    movement = addMoves(movement, function12(fireNodes[12], facing))
    killForward = functionKill(fireNodes[13], killing)


    
    return movement, killForward, fireNodes


    
    
class NeuralNetwork:
    

    # W_in_network = []
    # A_network = []
    pVals = []

    age = 0
    facing = 0
    lastMove = [0, 0 ,0]


    sensorVals = []

    
    def think(self, facing, xCoord, yCoord, environment_pop_density, environment_pheramones, barrierMask, distToBarrier, killing):
        self.sense(facing, xCoord, yCoord, environment_pop_density, environment_pheramones, barrierMask, distToBarrier)

        thought = self.applyMtx()
        thought = thought - 1.5
        
        movement, killForward,fireNodes = getAction(thought, self.facing)

        if killing:
            print(f'{sum(fireNodes)}')
            
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


    def applyMtx(self):
        self.sensorVals = np.random.rand(sensorNodeCount)
        
        # input = np.matmul(self.sensorVals, self.W_in_network)
        # idea = np.matmul(input, self.A_network)

        idea = np.matmul(self.sensorVals, W_A_Matmul)

        
        # print(f'pvals shape {self.pVals.shape}')
        # print(f'idea shape {idea.shape}')
        output = np.matmul(idea, self.pVals)
        return output
        
        
                     
    
    
    
    def __init__(self, gene):
        # self.W_in_network = W_In
        # self.A_network = A_network
        self.pVals = gene
        
        

W_In = getWin(D_r)
A_network = getANetwork(D_r)

W_A_Matmul = np.matmul(W_In, A_network)
    
