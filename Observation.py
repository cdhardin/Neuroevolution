

print('imported Observation')
#Observe

from InitializationVariables import *
from NeuralNetwork import activationNodeCount, sensorNodeCount

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.cm as cm
import numpy as np
import networkx as nx

import warnings
import random
import graphviz


barrier_cmap = ListedColormap(['none', 'darkgray'])
alive_cmap = ListedColormap(['none', 'green'])

#0 East, 1 North, 2 West, 3 South
facingArr = np.array([[1,0], [0,-1], [-1,0], [0,1]])
    
    
def observe(environment, observed_Agents, barrierMask, survivalMask, colorScale, environment_pop_density, plotpts):
    for agent in observed_Agents:
        x = agent.xCoord
        y = agent.yCoord
        color = [tempColor * (255/(2*colorScale)) + 255/2 for tempColor in agent.color]

        giveWidth = range(-agent_radius,agent_radius+1)

        
        for x_ in giveWidth:
                for y_ in giveWidth:
                    at_x = (x+x_)%environment_xSize
                    at_y = (y+y_)%environment_ySize
                    
                    environment[at_x, at_y] = color   # Note: (y, x) to match NumPy array indexing
        #getEyes
        facingDir = [np.cos(agent.angle) *agent_radius, np.sin(agent.angle) *agent_radius]


        
        facingCoord_x = round(x + facingDir[0])%environment_xSize
        facingCoord_y = round(y + facingDir[1])%environment_ySize

        eyeColor = [.2, .5, .9]
        environment[facingCoord_x, facingCoord_y] = eyeColor

        #getCenter
        brainColor = [1, 1, 1]
        environment[x, y] = brainColor
    
    # Plot the grid with agents
    
    
    # plt.imshow(environment_pop_density | barrierMask, cmap='gray', vmin=0, vmax=1)

    plt.imshow(environment, interpolation='none')
    plt.imshow(barrierMask, cmap=barrier_cmap, alpha=0.8, interpolation='none')
    plt.imshow(survivalMask, cmap=alive_cmap, alpha=0.2, interpolation='none')
    for pts in plotpts:
        if pts[0] < environment_xSize and pts[1] < environment_ySize :
            if showRays : plt.plot(pts[1],pts[0],'ro', alpha = .4, markersize=1) 

    # Add grid lines for better visualization
    # plt.grid(True, which='both', color='black', linewidth=0.5)
    # if random.random() < .15:
    #     plt.savefig('visionSurvival')
    plt.show()
    
    
def getAgentAnalysis(agents):
    sensorbuckets = np.zeros(sensorNodeCount)
    activebuckets = np.zeros(activationNodeCount)
    weightbuckets = np.zeros(100)

    for agent in agents:
        for edge in agent.agentBrain.network:
            sensorbuckets[int(edge[0])-1] = sensorbuckets[int(edge[0])-1] + 1 
            activebuckets[int(edge[1])-1] = activebuckets[int(edge[1])-1] + 1 
            weightbuckets[int(edge[2])] = int(weightbuckets[int(edge[2])] + 1 )
    return sensorbuckets, activebuckets, weightbuckets

def printBucketAnalysis(sensorbuckets, activebuckets, weightbuckets):
    for i in range(len(activebuckets)):
        print(f'{activeBucketTypes[i]} has {activebuckets[i]}')

    print( ' - - - - - - - - ')
    for i in range(len(sensorbuckets)):
        print(f'{sensorTypes[i]} has {sensorbuckets[i]}')
        
activeBucketTypes = [
    'No Movement',
    'Move East',
    'Move North',
    'Move NorthEast',
    'Move West',
    'Move South',
    'Move SouthWest',
    'Move NorthWest',
    'Move SouthEast',
    'forward',
    'backwards',
    'turnCC',
    'turnC',
    'kill'
]

sensorTypes = [
    'getLoc_X',
    'getLoc_Y',
    'getBoundary_Dist_x',
    'getBoundary_Dist',
    'getBoundary_Dist_y',
    'getYouth',
    'getLast_Move_X',
    'getLast_Move_Y',
    'getPopulationForward',
    'getBarrierForward',
    'getPopulationDensity',
    'getPopulationGradient_xDirection',
    'getPopulationGradient_yDirection',
    'getOscilatorVal',
    'getAge',
    'getBarrierDistForward',
    'getFacingX',
    'getFacingY',
    'getRandom',
    'getPheramones',
    'getPheramonesForward',
    'getDistToBarrier'
]

def plotNeuralNetwork(agent):
    # Create a bipartite graph
    G = nx.Graph()

    # Add sensor and action nodes with bipartite attribute
    G.add_nodes_from(activeBucketTypes, bipartite=0, node_type='action')
    G.add_nodes_from(sensorTypes, bipartite=1, node_type='sensor')

    for edge in agent.agentBrain.network:
        sensor, action, strength = edge
        G.add_edge(sensorTypes[int(sensor)], activeBucketTypes[int(action)], weight=strength)

    # Separate nodes by bipartite set
    sensor_nodes = {node for node, data in G.nodes(data=True) if data['bipartite'] == 1}
    action_nodes = set(G) - sensor_nodes

    fig, ax = plt.subplots(figsize=(10, 20))

    # Customize edge thickness and color based on weights
    edges = G.edges(data=True)
    weights = [data['weight'] for _, _, data in edges]
    edge_colors = plt.cm.RdYlGn([(weight) / 100 for weight in weights])

    # Draw the bipartite graph with customized edge attributes
    pos = nx.bipartite_layout(G, sensor_nodes)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue',
            font_color='black', font_size=10, node_size=800,
            width=3, edge_color=edge_colors, edge_cmap=plt.cm.RdYlGn)

    # Display the plot
    plt.show()





def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
    """ Plots the population's average and best fitness. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.plot(generation, avg_fitness, 'b-', label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")

    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    plt.savefig(filename)
    if view:
        plt.show()

    plt.close()


def plot_spikes(spikes, view=False, filename=None, title=None):
    """ Plots the trains for a single spiking neuron. """
    t_values = [t for t, I, v, u, f in spikes]
    v_values = [v for t, I, v, u, f in spikes]
    u_values = [u for t, I, v, u, f in spikes]
    I_values = [I for t, I, v, u, f in spikes]
    f_values = [f for t, I, v, u, f in spikes]

    fig = plt.figure()
    plt.subplot(4, 1, 1)
    plt.ylabel("Potential (mv)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, v_values, "g-")

    if title is None:
        plt.title("Izhikevich's spiking neuron model")
    else:
        plt.title("Izhikevich's spiking neuron model ({0!s})".format(title))

    plt.subplot(4, 1, 2)
    plt.ylabel("Fired")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, f_values, "r-")

    plt.subplot(4, 1, 3)
    plt.ylabel("Recovery (u)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, u_values, "r-")

    plt.subplot(4, 1, 4)
    plt.ylabel("Current (I)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, I_values, "r-o")

    if filename is not None:
        plt.savefig(filename)

    if view:
        plt.show()
        plt.close()
        fig = None

    return fig


def plot_species(statistics, view=False, filename='speciation.svg'):
    """ Visualizes speciation throughout evolution. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.savefig(filename)

    if view:
        plt.show()

    plt.close()


def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False,
             node_colors=None, fmt='svg'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    # Attributes for network nodes.
    if graphviz is None:
        warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
        return

    # If requested, use a copy of the genome which omits all components that won't affect the output.
    if prune_unused:
        genome = genome.get_pruned_copy(config.genome_config)

    if node_names is None:
        node_names = {}

    assert type(node_names) is dict

    if node_colors is None:
        node_colors = {}

    assert type(node_colors) is dict

    node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'}

    dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled', 'shape': 'box', 'fillcolor': node_colors.get(k, 'lightgray')}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'lightblue')}

        dot.node(name, _attributes=node_attrs)

    used_nodes = set(genome.nodes.keys())
    for n in used_nodes:
        if n in inputs or n in outputs:
            continue

        attrs = {'style': 'filled',
                 'fillcolor': node_colors.get(n, 'white')}
        dot.node(str(n), _attributes=attrs)

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            # if cg.input not in used_nodes or cg.output not in used_nodes:
            #    continue
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            style = 'solid' if cg.enabled else 'dotted'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    dot.render(filename, view=view)

    return dot
