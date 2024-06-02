# Evolving Neural Network ABM

## Overview
This repository contains the final project for Complex Systems 530 - Simulation and Modeling. The project focuses on an Agent-Based Model (ABM) utilizing NeuroEvolution of Augmenting Topologies (NEAT) to evolve the neural networks of individual agents. This approach aims to create evolving brains for agents within the simulation.

## Structure
The project is organized into several Jupyter Notebooks, each focusing on a specific aspect of the model. Below is a breakdown of the files and their purposes:

### Main Simulation
- **530_final.ipynb**: The main notebook for running the simulations. It includes detailed instructions on setting parameters for each demo.
- **initializationVariables.ipynb**: Contains initial configuration settings and variables used in the simulations.

### NEAT Training
- **Neat_environment.ipynb**: Defines the environment in which the NEAT algorithm operates.
- **TrainBrain.ipynb**: Handles the training process for the neural networks.
- **NeatConfig.ipynb**: Contains configuration settings specific to the NEAT algorithm.

### Neural Network
- **NeuralNetworksNEAT.ipynb**: Implements the neural network structures used by the agents.

### Agent Class
- **AgentModule_res.ipynb**: Defines the agent class, including attributes and behaviors.

### Observation Functions
- **Observation.ipynb**: Contains functions for observing and recording the state of the simulation.

### Simulation Execution
- **Evolution.ipynb**: Notebook for running the simulation code, allowing for the execution and monitoring of evolutionary processes.

## Usage
To use the project, follow these steps:

1. **Open and run `530_final.ipynb` to start the main simulation**. Detailed instructions for setting parameters are provided within the notebook.

2. **Refer to `initializationVariables.ipynb` for initial settings and configurations**.

3. For detailed exploration or modification of specific components, you can refer to the corresponding notebooks listed above.
