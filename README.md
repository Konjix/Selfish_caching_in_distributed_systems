# `selfish_caching.py` Overview
### Description:
`selfish_caching.py` is the core script of the "Selfish Caching" project, encompassing the implementation of the Network class and various functions for modeling and analyzing caching strategies in computer networks.

### Key Features:
- **Network Class**: Represents a computer network with methods to generate adjacency matrices with randomly chosen values based on specified probabilities. Allows network creation from existing adjacency matrices.
- **Network Analysis**: Includes functions for network analysis such as calculating network costs and presenting neighbor information for each node.
- **Experiments and Simulations**: Facilitates conducting a series of experiments with various network configurations to examine the effectiveness of caching strategies.

### Usage:
The script serves as a foundation for exploring and analyzing various aspects of caching in computer networks. It is utilized for data generation, simulations, and analyzing outcomes in the context of studying the performance and efficacy of different caching strategies.

# `selfish_caching_solver.py` Overview
### Description:
`selfish_caching_solver.py` is designed to solve the optimization problem related to caching in computer networks, using the Gurobi solver. It automatically generates optimization models for different network sizes and probabilities, and then solves them to find optimal caching strategies.

### Key Features:
- **Network Data Loading**: Loads adjacency matrix from files representing different computer networks.
- **Optimization Model Creation**: Uses Gurobi to define mathematical models, incorporating various constraints and objectives.
- **Optimization Problem Solving**: Employs the Gurobi solver to find optimal solutions for given caching problems.
- **Result Recording**: Saves optimization results, including optimal caching strategies, to text files.

### Usage:
This script is run within the larger "Selfish Caching" project context and is used for experimental investigation of the performance of different caching strategies in computer networks.

# `selfish_caching_show_network.py` Overview
### Description:
`selfish_caching_show_network.py` is a script for generating visualizations of computer network graphs. It utilizes the networkx and matplotlib libraries to create and display graphs based on adjacency matrices.

### Key Features:
- **Adjacency Matrix Loading**: Loads the adjacency matrix from a file, representing the computer network's structure.
- **Network Graph Generation**: Uses networkx to create a network graph from the loaded adjacency matrix.
- **Graph Visualization**: Utilizes matplotlib for graph visualization, showing nodes, edges, and edge weights.
- **Graph Saving**: Saves the generated graph visualization to a PNG file.

### Usage:
This script is useful for analyzing and presenting the structure of computer networks, allowing for a visual representation of connections and weights between network nodes.

# `selfish_caching_save_stats.py` Overview
### Description:
`selfish_caching_save_stats.py` is a script for analyzing results from experiments in the "Selfish Caching" project. It processes experimental data, calculates various statistics like average and variance of costs, and then saves these results in a readable format.

### Key Features:
- **Experimental Data Processing**: Loads experiment results from text files.
- **Statistics Calculation**: Computes statistics such as average cost, cost variance, and minimum cost for each data set.
- **Results Saving**: Saves the results in text format for easy review and analysis.
- **Results Visualization**: Generates plots showing the cost distribution across different network configurations, saved as PNG images.

### Usage:
This script is useful for analyzing the performance and costs of different caching strategies in computer networks, allowing for an in-depth understanding and comparison of various approaches in the context of experiments.

# `selfish_caching_combine_stat.py` Overview
### Description:
`selfish_caching_combine_stat.py` is intended to aggregate statistics from multiple text files containing results from "Selfish Caching" experiments. The goal is to create a unified dataset for easier analysis and comparison.

### Key Features:
- **Data Collection**: Searches a specified folder for statistic files and loads data from each file.
- **Statistics Aggregation**: Combines the gathered information into a single comprehensive file, facilitating further analysis.
