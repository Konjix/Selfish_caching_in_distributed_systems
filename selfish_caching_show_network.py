import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#network_sizes = [10, 15, 25, 50]
#network_probabilities = [2, 3, 4] # 50%, 33%, 25%

network_sizes = [15]
network_probabilities = [4] # 50%, 33%, 25%

for network_size in network_sizes:
    for network_probability in network_probabilities:
        path = f"network_{network_size}_{network_probability}"

        if os.path.exists(f"Experiment_results\\Networks"):
            file_path = f"Experiment_results\\Networks\\{path}.txt" 
        try:
            adjacency_matrix = np.loadtxt(file_path, delimiter=",", dtype=int)
        except Exception as e:
            print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')

        G = nx.Graph()
        G.add_nodes_from(range(network_size))

        for i in range(network_size):
            for j in range(i + 1, network_size):
                if adjacency_matrix[i, j] != 0:
                    G.add_edge(i, j, weight=adjacency_matrix[i, j])

        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', font_family='sans-serif', edge_color='gray', width=2, edge_cmap=plt.cm.Blues)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        if not os.path.exists(f"Experiment_results\\Show"):
            os.makedirs(f"Experiment_results\\Show")
        plt.savefig(f"Experiment_results\\Show\\{path}_graph.png")
