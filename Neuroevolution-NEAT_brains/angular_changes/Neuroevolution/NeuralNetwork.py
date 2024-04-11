print('imported Neural Network module')
import numpy as np
from numpy.linalg import eigvals

import os
import neat

import random 
from InitializationVariables import *
from NodeFunctions import *

activationNodeCount = 7
sensorNodeCount = 10 + 2 * numRays 


local_dir = os.getcwd()  # Get the current working directory
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                 config_path)




def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def shouldFire(arr):

    arr = np.array(arr)
    if Softmax_on: 
        input = softmax(arr)
        sigmoid = np.tanh(input)
    else: 
        sigmoid = np.tanh(arr)

    
    random_array = np.random.rand(*arr.shape)
    fire = random_array<sigmoid

    # print(sum(fire)) ##CDH
    return fire





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
    


    net = None

    age = 0
    angle = 0
    lastMove = [0, 0 ,0]


    sensorVals = []

    
    def think(self, theta, omega, xCoord, yCoord, barrierMask, killing, environment_pop_density, survivalMask):
        plotpoints = self.sense(theta, omega, xCoord, yCoord,killing, environment_pop_density, barrierMask, survivalMask)

        thought = self.net.activate(self.sensorVals)

        
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
      
    
    def __init__(self, gene):

        
        self.net = neat.nn.FeedForwardNetwork.create(gene, config)

        
        


    
