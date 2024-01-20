from gurobipy import Model, GRB, quicksum
import os
import numpy as np

if not os.path.exists(f"Experiment_results\\Optimum"):
    os.makedirs(f"Experiment_results\\Optimum")

exp_network_sizes = [10, 15, 25, 50]
exp_network_probabilities = [2, 3, 4]

for network_size in exp_network_sizes:
    for network_probability in exp_network_probabilities:

        path = f"network_{network_size}_{network_probability}"
        file_path = f"Experiment_results\\Networks\\{path}.txt"
        
        if os.path.exists(file_path):
            try:
                adjacency_matrix = np.loadtxt(file_path, delimiter=",", dtype=int)
                print(adjacency_matrix)
                m = Model('optimum_social')

                # Create variables
                x = m.addVars(network_size, vtype=GRB.BINARY, name="strategy_vector")
            
                # Objective function
                obj = quicksum(network_size * x[i] for i in range(network_size))
                for i in range(network_size):
                    for k in range(network_size):
                        if adjacency_matrix[i][k] != 0:
                            obj += adjacency_matrix[i][k] * (1 - x[i])
                m.setObjective(obj, GRB.MINIMIZE)
                
                # Constraints
                for i in range(network_size):
                    neighbours = [i]
                    for j in range(network_size):
                        if adjacency_matrix[i][j] > 0:
                            neighbours.append(j)
                    print(f"Neighbours for {i}: {neighbours}")
                    sum = quicksum(x[k] for k in neighbours)
                    print(sum)
                    m.addConstr(sum >= 1)
                
                for i in range(network_size):
                    for k in range(network_size):
                        if adjacency_matrix[i][k] != 0:
                            m.addConstr(x[i] + x[k] <= 1)
                
                # Optimize model
                m.optimize()

                # Output results
                if m.status == GRB.OPTIMAL:
                    # Output results
                    solution_x = [abs(int(v.X)) for v in x.values()]
                    optimum_file_path = f"Experiment_results\\Optimum\\{path}_optimum.txt"
                    with open(optimum_file_path, "w") as optimum_file:
                        optimum_file.write(",".join(map(str, solution_x)))
                else:
                    print(f"Model not solved to optimality. Status: {m.status}")

                
            except Exception as e:
                print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')
