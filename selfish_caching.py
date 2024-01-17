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
    
    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix):
        size = len(adjacency_matrix)
        network = cls(size)
        for i in range(size):
            for j in range(i + 1, size):
                network.matrix[i, j, 0] = adjacency_matrix[i, j]
                network.matrix[j, i, 0] = adjacency_matrix[i, j]
        return network
    
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
    
    def network_cost(self):
        cost = 0
        for i in range(self.size):
            cost += self.matrix[i, i, 0]
        return cost
    
    def save_to_file(self, file_path):
        shape_3d = self.matrix.shape
        matrix_2d = self.matrix[:, :, 0].reshape(shape_3d[0], shape_3d[1])
        np.savetxt(file_path, matrix_2d, fmt="%d", delimiter=", ")

def generate_initial_strategy_array_with_ones(size):
    strategy_array = np.zeros(size)
    for i in range(size):
        strategy_array[i] = 1

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
        cost_2 = neighbor_min_cost(network, current_strategy, current_node)
        print(cost_2)
        cost_min = min(cost_1, cost_2)
        if new_network.matrix[current_node, current_node, 0] > cost_min:
            print(f'found better, current_node {current_node}')
            new_network.matrix[current_node, current_node, 0] = cost_min;
            if cost_min == cost_1:
                
                new_strategy[current_node] = 1
            else:
                new_strategy[current_node] = 0
            return False, new_network, new_strategy
    return True, network, current_strategy


def neighbor_min_cost(network, current_strategy, current_node):
    num_nodes = len(current_strategy)
    cost_min = sys.maxsize
    
    for neighbor_id in range(num_nodes):
        if(network.matrix[current_node, neighbor_id, 0] != 0 and current_strategy[neighbor_id] == 1 and current_node != neighbor_id):
            download_cost = network.matrix[current_node, neighbor_id, 0]
            if  download_cost < cost_min:
                cost_min = download_cost
    return cost_min


def selfish_caching_iterations(network, strategy, file=None):
    n = 1
    while True:
        stop, network, strategy = update_strategy(network, strategy)
        if file:
            with open(file, "a") as f:
                f.write(f"Strategy for iteration {n}: {strategy}\n")
                f.write(f"Cost of network for iteration {n}: {network.network_cost()}\n\n")
        n+=1
        if stop:
            return network, strategy, n


# Experiment
def experiment():
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
                    exp_network, exp_strategy, exp_iterations = selfish_caching_iterations(exp_network, exp_strategy)
                    exp_network_results.append([network_objects, exp_network.network_cost(), exp_iterations])
            exp_network_results_str = np.array(exp_network_results, dtype=str)
            np.savetxt(f"{output_folder}\\Results\\experiment_results_{network_size}_{network_probabilities}.txt",
                        exp_network_results, fmt="%s", delimiter=",")


# Show run
def show_run():
    show_network_size = 10
    show_network_probability = 2
    show_network_objects = 5

    path = f"network_{show_network_size}_{show_network_probability}"

    if not os.path.exists(f"Experiment_results\\Show"):
        os.makedirs(f"Experiment_results\\Show")
    output_file = f"Experiment_results\\Show\\{path}_run_.txt"

    if os.path.exists(f"Experiment_results\\Networks"):
        file_path = f"Experiment_results\\Networks\\{path}.txt"
    try:
        adjacency_matrix = np.loadtxt(file_path, delimiter=",", dtype=int)
    except Exception as e:
        print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')

    show_network = Network.from_adjacency_matrix(adjacency_matrix)
    #show_strategy = generate_initial_strategy_array_random(show_network_size, show_network_objects)
    #show_strategy = generate_initial_strategy_array_with_ones(show_network_size)
    show_strategy = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    show_network.initial_network_costs(show_strategy)

    with open(output_file, 'w') as f:
        f.write(f"Initial strategy: {show_strategy}\n")
        f.write(f"Initial cost of network: {show_network.network_cost()}\n\n")

    show_network, show_strategy, show_iterations = selfish_caching_iterations(show_network, show_strategy, output_file)

    with open(output_file, 'a') as f:
        f.write(f"Final strategy: {show_strategy}\n")
        f.write(f"Final cost of network: {show_network.network_cost()}")


if __name__ == '__main__':
    show_run()