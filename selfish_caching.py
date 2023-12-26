import numpy as np
import sys
import os


class Network:
    def __init__(self, size):
        self.size = size
        self.matrix = np.zeros((size, size, 2), dtype=int)

    def populate_random_values(self, probability):
        for col in range(self.size):
            self.matrix[:, col, 0] = np.random.randint(0, probability, size=self.size)
        for col in range(self.size):
            for row in range(col, self.size):
                if(self.matrix[row, col, 0] == (probability - 1) and row != col):
                    self.matrix[row, col, 0] = np.random.randint(1, self.size)
                    self.matrix[col, row, 0] = self.matrix[row, col, 0]
                else:
                    self.matrix[row, col, 0] = 0
                    self.matrix[col, row, 0] = 0
    
    def present_network(self, print_neighbors):
        for node_id in range(self.size):
            if (print_neighbors):
                print(f"Node {node_id + 1} - Neighbors:")
                for neighbor_id in range(self.size):
                    if (self.matrix[node_id][neighbor_id][0] != 0 and neighbor_id != node_id):
                        print(f"\tNode {neighbor_id + 1}, route cost: {self.matrix[node_id][neighbor_id][0]}")
    
    def initial_network_costs(self, initial_strategy):
        for node_id in range(self.size):
            if initial_strategy[node_id] == 1:
                self.matrix[node_id, node_id, 0] = self.size
                self.matrix[node_id, node_id, 1] = node_id
            else:
                self.matrix[node_id, node_id, 0] = -1
                self.matrix[node_id, node_id, 1] = -1
                
        # Find 1st level of neighbours
        for node_id in range(self.size):
            if(initial_strategy[node_id] == 0):
                for neighbor_id in range(self.size):
                    if(initial_strategy[neighbor_id] == 1 and self.matrix[node_id, neighbor_id, 0] != 0
                    and neighbor_id != node_id):
                        self.matrix[node_id, node_id, 0] = self.matrix[node_id, neighbor_id, 0]
                        self.matrix[node_id, node_id, 1] = neighbor_id
        # Next levels of neighbours
        continue_filling = True
        while continue_filling:
            continue_filling = False
            for node_id in range(self.size):
                if(initial_strategy[node_id] == 0 and self.matrix[node_id, node_id, 0] == -1):
                    for neighbor_id in range(self.size):
                        if(self.matrix[node_id, neighbor_id, 0] != 0 and neighbor_id != node_id):
                            self.matrix[node_id, node_id, 0] = self.matrix[node_id, neighbor_id, 0] + self.matrix[neighbor_id, neighbor_id, 0]
                            self.matrix[node_id, node_id, 1] = self.matrix[node_id, neighbor_id, 1]
                            continue_filling = True
    
    def network_cost(self):
        cost = 0
        for i in range(self.size):
            cost += self.matrix[i, i, 0]
        return cost
    
    def save_to_file(self, file_path):
        shape_3d = self.matrix.shape
        matrix_2d = self.matrix[:, :, 0].reshape(shape_3d[0], shape_3d[1])
        np.savetxt(file_path, matrix_2d, fmt="%d", delimiter=", ")


def generate_initial_strategy_array(size):
    strategy_array = np.random.choice([0, 1], size=size)
    
    return strategy_array


def generate_initial_strategy_array_with_zeros(size, place):
    strategy_array = np.zeros(size)
    strategy_array[place] = 1
    strategy_array[place - 1] = 1

    return strategy_array


def generate_initial_strategy_array_random(size, objects):
    strategy_array = np.zeros(size, dtype=int)
    random_array = np.random.choice(size, size=objects, replace=False)
    for i in range(objects):
        strategy_array[random_array[i]] = 1

    return strategy_array


def update_strategy(network, current_strategy):
    new_network = Network(network.size)
    new_network.matrix = np.copy(network.matrix)
    new_strategy = current_strategy.copy()
    num_nodes = len(current_strategy)
    
    for current_node in range(num_nodes):
        cost_1 = num_nodes
        cost_2, cost_2_node = neighbor_min_cost(network, current_strategy, current_node)
        cost_min = min(cost_1, cost_2)
        if new_network.matrix[current_node, current_node, 0] > cost_min:
            if cost_min == cost_1:
                new_network.matrix[current_node, current_node, 0] = cost_min;
                new_strategy[current_node] = 1
                new_network.matrix[current_node, current_node, 1] = current_node;
                return False, new_network, new_strategy
            elif current_node != new_network.matrix[cost_2_node, cost_2_node, 1]:
                new_network.matrix[current_node, current_node, 0] = cost_min;
                new_strategy[current_node] = 0
                new_network.matrix[current_node, current_node, 1] = cost_2_node;
                if current_strategy[current_node] == 1:
                    for check_back_node in range(num_nodes):
                        if new_network.matrix[check_back_node, check_back_node, 1] == current_node and check_back_node != current_node:                            
                            check_back_cost, check_back_node_from = neighbor_min_cost(new_network, new_strategy, check_back_node)
                            new_network.matrix[check_back_node, check_back_node, 0] = check_back_cost
                            new_network.matrix[check_back_node, check_back_node, 1] = check_back_node_from
                return False, new_network, new_strategy
            
    return True, network, current_strategy


def neighbor_min_cost(network, current_strategy, current_node):
    num_nodes = len(current_strategy)
    cost_min = sys.maxsize
    download_from = num_nodes + 1
    
    for neighbor_id in range(num_nodes):
        if(network.matrix[current_node, neighbor_id, 0] != 0):
            download_cost = network.matrix[current_node, neighbor_id, 0]
            if current_strategy[neighbor_id] == 0:
                download_cost += network.matrix[neighbor_id, neighbor_id, 0]
            if  download_cost < cost_min:
                cost_min = download_cost
                download_from = network.matrix[neighbor_id, neighbor_id, 1]     
    return cost_min, download_from


def selfish_caching_iterations(network, strategy, show):
    n = 1
    while True:
        stop, network, strategy = update_strategy(network, strategy)
        if show:
            print (f"\nStrategy and costs for iteration {n}: {strategy}")
            network.present_network(False)
            print()
        n+=1
        if stop:
            return network, strategy, n


'''
# Test
network_size = 10

strategy = generate_initial_strategy_array_with_zeros(network_size, 0)
network = Network(network_size)
network.populate_random_values(1)
network.initial_network_costs(strategy)

print(f"Initial strategy: {strategy}")
network.present_network(True)

network, strategy, iterations = selfish_caching_iterations(network, strategy, True)
    
print(f"Final strategy: {strategy}")
network.present_network(False)
'''
'''
# Proof of concept
test_network_size = 10
test_network = Network(test_network_size)
test_network.populate_random_values(2)
test_network.present_network(True)
for i in range(test_network_size):
    # test_strategy = generate_initial_strategy_array_with_zeros(test_network_size, i)
    test_strategy = generate_initial_strategy_array_random(test_network_size, 10)
    print(f"Initial strategy: {test_strategy}")
    test_network.initial_network_costs(test_strategy)
    test_network, test_strategy, iterations = selfish_caching_iterations(test_network, test_strategy, False)
    print(f"Number of iterations to balance network for object placed at node {i + 1}: {iterations}")
    print(f"Final strategy: {test_strategy}")
    print(f"Network cost: {test_network.network_cost()}")
'''

# Experiment
output_folder = "Experiment_results"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
subfolders = ["Networks", "Results"]
for subfolder in subfolders:
    subfolder_path = os.path.join(output_folder, subfolder)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)



exp_network_sizes = [10, 15, 25, 50]
exp_network_probabilities = [2, 3, 4] # 50%, 33%, 25%
exp_network_objects = [2, 5, 10]

for network_size in exp_network_sizes:
    for network_probabilities in exp_network_probabilities:
        exp_network = Network(network_size)
        exp_network.populate_random_values(network_probabilities)
        exp_network.save_to_file(f"{output_folder}\\Networks\\network_{network_size}_{network_probabilities}.txt")
        exp_network_results = []
        exp_network_results.append(["Objects", "Cost", "Iterations"])
        for i in range(network_size):
            for network_objects in exp_network_objects:
                exp_strategy = generate_initial_strategy_array_random(network_size, network_objects)
                exp_network.initial_network_costs(exp_strategy)
                exp_network, exp_strategy, exp_iterations = selfish_caching_iterations(exp_network, exp_strategy, False)
                exp_network_results.append([network_objects, exp_network.network_cost(), exp_iterations])
        exp_network_results_str = np.array(exp_network_results, dtype=str)
        np.savetxt(f"{output_folder}\\Results\\experiment_results_{network_size}_{network_probabilities}.txt",
                    exp_network_results, fmt="%s", delimiter=",")