from gurobipy import Model, GRB
import os

import numpy as np

if not os.path.exists(f"Experiment_results\\Optimum"):
    os.makedirs(f"Experiment_results\\Optimum")

exp_network_sizes = [10, 15, 25, 50]
exp_network_probabilities = [2, 3, 4]

for network_size in exp_network_sizes:
    for network_probability in exp_network_probabilities:

        path = f"network_{network_size}_{network_probability}"

        if os.path.exists(f"Experiment_results\\Networks"):
            file_path = f"Experiment_results\\Networks\\{path}.txt"
            
        try:
            adjacency_matrix = np.loadtxt(file_path, delimiter=",", dtype=int)
            m = Model('optimum_social')

            # Create variables
            x = m.addVars(network_size, vtype=GRB.BINARY, name="strategy_vector")  # Binary decision variable x_ij

            # Since there's only one object and demand is always 1, we can simplify the constraints and objective function

            # Objective function: Minimize the sum of distances for the chosen paths
            m.setObjective(sum(network_size * x[i] + sum(adjacency_matrix[i][k] * (1 - x[i]) for k in range(network_size)) for i in range(network_size)),GRB.MINIMIZE)

            '''
            # Constraint 1: Each server must get the object from exactly one server
            for i in range(n):
                m.addConstr(sum(x[k] for k in range(n) if network[i][k] != 0) == 1)
            '''
            # Constraint 2: Simplified since we only deal with one object and y_ijk is 1 - x_ij
            # If object is taken from server k by server i, it cannot be stored on server i
            for i in range(network_size):
                for k in range(network_size):
                    if adjacency_matrix[i][k] != 0:
                        m.addConstr(x[i] + x[k] <= 1)

            # Constraint 3 and 4: Already defined by the variable types (binary)

            # Optimize model
            m.optimize()

            # Output results
            solution_x = []
            for v in m.getVars():
                solution_x.append(abs(int(v.x)))
            optimum_file_path = f"Experiment_results\\Optimum\\{path}_optimum.txt"
            with open(optimum_file_path, "w") as optimum_file:
                for i in range(network_size):
                    optimum_file.write(f"{solution_x[i]}")
                    if i < network_size-1:
                        optimum_file.write(",")
        except Exception as e:
            print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')
            continue