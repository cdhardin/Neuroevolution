print('imported Neural Network module')
import numpy as np
from numpy.linalg import eigvals

import random 
from InitializationVariables import *
from NodeFunctions import *

activationNodeCount = 7
sensorNodeCount = 10 + 2 * numRays 




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



def getWin(D_r):
    N = sensorNodeCount
    M = D_r
    p = .2
    np.random.seed(41544)
    return np.random.choice([0, 1], size=(N, M), p=[1-p, p])


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def shouldFire(arr):

    arr = np.array(arr)
    input = softmax(arr)
    sigmoid = np.tanh(input)
    random_array = np.random.rand(*arr.shape)
    fire = random_array<sigmoid

    # print(sum(fire)) ##CDH
    return fire



def addMoves(move1, move2):
    move = [0, 0, 0]
    move[0] = move1[0] + move2[0]
    move[1] = move1[1] + move2[1]
    move[2] = move1[2] + move2[2]
    return move



def getAction(thought):


    fireNodes = shouldFire(thought)
    
    

    # print(f' Firing nodes: {fireNodes}')
    
    changeAngle = updateAngle(fireNodes[0]) - updateAngle(fireNodes[1])
    changeAngularVelocity = updateAngularVelocity(fireNodes[2]) - updateAngularVelocity(fireNodes[3])
    changeVelocity = updateVelocity(fireNodes[4]) - updateVelocity(fireNodes[5])


    

    movement = [changeAngle, changeAngularVelocity, changeVelocity] 
    
    killForward = functionKill(fireNodes[-1], killing)


    
    return movement, killForward, fireNodes


    
    
class NeuralNetwork:
    

    # W_in_network = []
    # A_network = []
    pVals = []

    age = 0
    angle = 0
    lastMove = [0, 0 ,0]


    sensorVals = []

    
    def think(self, theta, omega, xCoord, yCoord, barrierMask, killing, environment_pop_density, survivalMask):
        plotpoints = self.sense(theta, omega, xCoord, yCoord,killing, environment_pop_density, barrierMask, survivalMask)

        thought = self.applyMtx()
        
        movement, killForward,fireNodes = getAction(thought)


        if killing:
            print(f'{sum(fireNodes)}')
            
        return movement, killForward, plotpoints


    
    
    def sense(self, theta, omega, xCoord, yCoord,killing, environment_pop_density, barrierMask, survivalMask):
        self.age = self.age + 1
        
        sensorVals = [
            getLoc_X(xCoord),
            getLoc_Y(yCoord),
            getBoundary_Dist_x(xCoord),
            getBoundary_Dist_y(yCoord),
            getOscilatorVal(self.age),
            getAge(self.age),
            getRandom(),
            seeAngularVelocity(omega) 
        ]

        sensorVals.append(self.angle % (2*np.pi) / (2*np.pi) )
        sensorVals.append( (self.angle + np.pi) % (2*np.pi) / (2*np.pi) )

       
        plotpoints = []
        angles = np.linspace(-angleMax, angleMax, numRays)
        for angle in angles:
            results = rayDist(xCoord, yCoord, theta, angle, environment_pop_density, barrierMask, survivalMask) 

            distRatio = (vision_distance - results[0]) / vision_distance
            safetydistRatio = ( vision_distance - results[2]) / vision_distance
            
            sensorVals.append(distRatio)
            sensorVals.append(safetydistRatio)


            
            plotpoints += results[1]

       
        
        self.sensorVals = sensorVals
        return plotpoints


    def applyMtx(self):
        # self.sensorVals = np.random.rand(sensorNodeCount)
        
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
    
