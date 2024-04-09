print('Imported initialized Variables')
from numpy import pi

# X-Y length of environment grid
environment_xSize = 400
environment_ySize = 400

# Wrapping on environment, 1 - on : 0 - off
xWrapping = 0 
yWrapping = 0

agent_count = 10

steps_per_cycle = 100
numGenerations = 400
plot_freq = 1

network_edges = 10
D_r = 120

agent_radius = 4
vision_distance = environment_xSize

#For Rays:
angleMax = pi/4
numRays = 7
showRays = False

maxVelocity = 4
maxAngularVelocity = pi/6

collisionKillsBoth = False

mutation_chance = 0.1

killing = False
collisionsKill = False

pheramoneDecayRate = .5 #How much pheramones decay each step

# How much of an effect comes from 1 agent
pheramoneScale = 50
popScale = 50

monogamous = 0 # 1 - each agent reproduce with one random agent x times : 0 - each agent reproduce with x random agents one time
