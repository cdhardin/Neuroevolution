print('imported eval_genome')
from InitializationVariables import *
from Simulation import * 
from numpy import mean

def eval_genome(genome, config):
    fitnesses = []

    for runs in range(runs_per_net):

        fitness = RunSim(genome)
        

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return mean(fitnesses)
