from AgentModule import *
from Environment import *
from Observation import *
from InitializationVariables import *
# from Simulation import * 


from IPython import display
import time


print('imported evolution module')

def initializeAgents(agent_count, agents, gene):
    if not agents:
        agents = []
    for i in range(agent_count):
        agent_instance = Agent(id=(i+1), gene=gene, xCoord = random.randint(0, environment_xSize - 1), yCoord=random.randint(environment_ySize/4, environment_ySize - 1)) ##CDH
        agents.append(agent_instance)
    return agents


def runCycle(steps_per_cycle, agents, environment, barrierMask,distToBarrier, survivalMask, environment_pop_density, killing):
    colorScale = getColorScale(agents)
    for i in range(steps_per_cycle):
        plotpts = operateAll(agents, barrierMask, distToBarrier, environment_pop_density,  killing, survivalMask)
        
        observe(environment, agents, barrierMask, survivalMask, colorScale,environment_pop_density, plotpts)
        environment = resetEnv(environment)
        
        environment_pop_density = getPopDensity(environment_pop_density, agents)
        
        display.clear_output(wait=True)
        time.sleep(0.01)#CDH
    livingAgents, killcount = collectLivingAgents(agents, survivalMask)
    environment = resetEnv(environment)
    return livingAgents, environment, killcount

def simCycle(steps_per_cycle, agents, environment, barrierMask, distToBarrier, survivalMask, environment_pop_density, killing):
    for i in range(steps_per_cycle):
        operateAll(agents, barrierMask, distToBarrier, environment_pop_density,  killing, survivalMask)
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
    if survivors == 0 :
        print('extinct')
        return None
    reproduction_rate = agent_count / survivors
    if monogamous : 
        for agent in livingAgents:
            partner = livingAgents[random.randint(0, survivors-1)]
            for i in range(round(reproduction_rate)):
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
    gene1 = gene1.T
    gene2 = gene2.T

    gene_merged = np.zeros(gene1.shape)

    for i in range(len(gene1)):
        if i%2 ==0 :
            gene_merged[i] = gene1[i]
        else :
            gene_merged[i] = gene2[i]

        if random.random() < mutation_chance:
            gene_merged[i] = np.zeros(gene_merged[i].shape)
            
            non_zero_indices = np.random.choice(len(gene_merged[i]), 3, replace=False)
            gene_merged[i,non_zero_indices] = np.random.rand(3) 
            gene_merged[i] = gene_merged[i]/sum(gene_merged[i])
    
    return gene_merged.T


def getStartGene():
    N = D_r
    M = activationNodeCount

    matrix = np.zeros((N, M))
    for j in range(M):
        non_zero_indices = np.random.choice(N, 3, replace=False)
        matrix[non_zero_indices, j] = np.random.rand(3) 
    
    # Normalize each Row so that its elements sum to 1
    matrix /= matrix.sum(axis=0, keepdims=True)
    return matrix





def getColorScale(agents):
    maxVal = 1
    for agent in agents:
        thisVal = np.max(np.abs(agent.color))
        if thisVal > maxVal: maxVal = thisVal
    return maxVal

def getGeneticSimilarity(agents1, agents2):
    avgBrain1 = np.zeros(agents1[0].agentBrain.pVals.T.shape)
    avgBrain2 = np.zeros(agents2[0].agentBrain.pVals.T.shape)

    for agent in agents1:
        avgBrain1 += agent.agentBrain.pVals.T
    avgBrain1 = avgBrain1/len(agents1)

    for agent in agents2:
        avgBrain2 += agent.agentBrain.pVals.T
    avgBrain2 = avgBrain2/len(agents2)
    
    return sum( (sum(avgBrain1)- sum(avgBrain2)) **2)



