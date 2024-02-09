print('Imported initialized Variables')

# X-Y length of environment grid
environment_xSize = 300
environment_ySize = 300

# Wrapping on environment, 1 - on : 0 - off
xWrapping = 0 
yWrapping = 0

agent_count = 1000

steps_per_cycle = 30
numGenerations = 10
plot_freq = 1

network_edges = 10

mutation_chance = 0.35

killing = False

pheramoneDecayRate = .5 #How much pheramones decay each step

# How much of an effect comes from 1 agent
pheramoneScale = 50
popScale = 50

monogamous = 1 # 1 - each agent reproduce with one random agent x times : 0 - each agent reproduce with x random agent one time
