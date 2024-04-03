print('Imported initialized Variables')

# X-Y length of environment grid
environment_xSize = 700
environment_ySize = 700

# Wrapping on environment, 1 - on : 0 - off
xWrapping = 0 
yWrapping = 0

agent_count = 200

steps_per_cycle = 50
numGenerations = 800
plot_freq = 1

network_edges = 10
D_r = 100

agent_radius = 5

collisionKillsBoth = True

mutation_chance = 0.1

killing = False
collisionsKill = True

pheramoneDecayRate = .5 #How much pheramones decay each step

# How much of an effect comes from 1 agent
pheramoneScale = 50
popScale = 50

monogamous = 0 # 1 - each agent reproduce with one random agent x times : 0 - each agent reproduce with x random agents one time
