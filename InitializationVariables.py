print('Imported initialized Variables')
from numpy import pi


##IMPORTANT PARAMETERS FOR 530 FINAL

# X-Y length of environment grid

environment_xSize = 300
environment_ySize = 300

agent_radius = 5
vision_distance = environment_ySize

showRays = True #If true - visualizes the vision rays of agents. (RUNS MUCH SLOWER)

collisionKillsBoth = False #Do agents die if they collide with each other

agent_count = 10
steps_per_cycle = 200
maxVelocity = 5







##END IMPORTANT PARAMS

# Wrapping on environment, 1 - on : 0 - off
xWrapping = 0 
yWrapping = 0


numGenerations = 1
plot_freq = 1


## FOR NEAT
runs_per_net = 2
simulation_seconds = 60.0


network_edges = 10
D_r = 120



#For Rays:
angleMax = pi/3
numRays = 7

maxAngularVelocity = pi/6


Softmax_on = False


mutation_chance = 0.1

killing = False
collisionsKill = False

pheramoneDecayRate = .5 #How much pheramones decay each step

# How much of an effect comes from 1 agent
pheramoneScale = 50
popScale = 50

monogamous = 0 # 1 - each agent reproduce with one random agent x times : 0 - each agent reproduce with x random agents one time
