from AgentModule import *
from Environment import *
from Observation import *
from InitializationVariables import *

from IPython import display
import time


print('imported evolution module')

def initializeAgents(agent_count, agents = None):
    if not agents:
        agents = []
    for i in range(agent_count):
        agent_instance = Agent(id=(i+1), gene=getStartGene(), xCoord = random.randint(0, environment_xSize - 1), yCoord=random.randint(0, environment_ySize - 1))
        agents.append(agent_instance)
    return agents


def runCycle(steps_per_cycle, agents, environment, barrierMask,distToBarrier, survivalMask, environment_pop_density, environment_pheramones, killing):
    colorScale = getColorScale(agents)
    for i in range(steps_per_cycle):
        operateAll(agents, barrierMask, distToBarrier, environment_pop_density, environment_pheramones, killing)
        observe(environment, agents, barrierMask, survivalMask, colorScale)
        environment = resetEnv(environment)
        environment_pop_density = getPopDensity(environment_pop_density, agents)
        environment_pheramones = getPheramones(environment_pheramones, agents)
        display.clear_output(wait=True)
        time.sleep(0.1)
    livingAgents, killcount = collectLivingAgents(agents, survivalMask)
    environment = resetEnv(environment)
    return livingAgents, environment, killcount

def simCycle(steps_per_cycle, agents, environment, barrierMask, distToBarrier, survivalMask, environment_pop_density, environment_pheramones, killing):
    for i in range(steps_per_cycle):
        operateAll(agents, barrierMask, distToBarrier, environment_pop_density, environment_pheramones, killing)
        environment = resetEnv(environment)
    livingAgents, killcount = collectLivingAgents(agents, survivalMask)
    environment = resetEnv(environment)
    return livingAgents, environment, killcount


def collectLivingAgents(agents, survivalMask):
    livingAgents = []
    killCount = 0
    for agent in agents:
        if not agent.dead:
            if survivalMask[agent.xCoord][agent.yCoord] : livingAgents.append(agent)
        else: killCount += 1
    return livingAgents, killCount



def repopulateAgents(livingAgents, monogamous):
    nextGenAgents = []
    survivors = len(livingAgents)
    reproduction_rate = agent_count / survivors
    if monogamous : 
        for agent in livingAgents:
            partner = livingAgents[random.randint(0, survivors-1)]
            for i in range (round(reproduction_rate)):
                child = breed(agent, partner)
                nextGenAgents.append(child)
    else :
        for agent in livingAgents:
            for i in range (round(reproduction_rate)):
                partner = livingAgents[random.randint(0, survivors-1)]
                child = breed(agent, partner)
                nextGenAgents.append(child)
                
    return nextGenAgents

def avg_int(a, b):
    return (a+b)%agent_count

def breed(agent1, agent2):
    child = Agent(avg_int(agent1.id, agent2.id), mutate(agent1.gene,agent2.gene), xCoord = random.randint(0, environment_xSize - 1), yCoord=random.randint(0, environment_ySize - 1))
    return child


def mutate(gene1, gene2):
    gene1_str = str(gene1)
    gene2_str = str(gene2)
    
    if(random.random() < mutation_chance):
        mutation_spot = random.randint(0,len(gene1_str)-1)
        mutation_char = str(random.randint(0,9))
        if mutation_spot == 0:
            if mutation_char == '0' : mutation_spot = random.randint(1,len(gene1_str)-1)
        gene1_str = gene1_str[:mutation_spot] + mutation_char + gene1_str[mutation_spot + 1:]
        
    if(random.random() < mutation_chance):
        mutation_spot = random.randint(0,len(gene2_str)-1)
        mutation_char = str(random.randint(0,9))
        gene2_str = gene2_str[:mutation_spot] + mutation_char + gene2_str[mutation_spot + 1:]
    
    gene_merged = int(gene1_str[:int((len(gene1_str))/2)] + gene2_str[int((len(gene1_str))/2) :] )
    
    return gene_merged

def getStartGene():
    digits = 6 * network_edges 
    gene = random.randint(0, pow(10, digits))
    return gene


def getColorScale(agents):
    maxVal = 1
    for agent in agents:
        thisVal = np.max(np.abs(agent.color))
        if thisVal > maxVal: maxVal = thisVal
    return maxVal
