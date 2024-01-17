from gurobipy import Model, GRB

# Define the network as a matrix (cost from server i to server k)

network = [
    [0, 0, 8, 0, 1, 0, 6, 0, 3, 7],
    [0, 0, 0, 5, 3, 1, 0, 0, 5, 0],
    [8, 0, 0, 6, 0, 0, 1, 4, 0, 0],
    [0, 5, 6, 0, 0, 0, 0, 0, 0, 5],
    [1, 3, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 6, 0],
    [6, 0, 1, 0, 0, 0, 0, 1, 8, 6],
    [0, 0, 4, 0, 1, 0, 1, 0, 0, 9],
    [3, 5, 0, 0, 0, 6, 8, 0, 0, 7],
    [7, 0, 0, 5, 1, 0, 6, 9, 7, 0]
]

# Number of servers
n = len(network)

# Create a new model
m = Model('optimum_social')

# Create variables
x = m.addVars(n, vtype=GRB.BINARY, name="strategy_vector")  # Binary decision variable x_ij

# Since there's only one object and demand is always 1, we can simplify the constraints and objective function

# Objective function: Minimize the sum of distances for the chosen paths
m.setObjective(sum(n * x[i] + sum(network[i][k] * (1 - x[i]) for k in range(n)) for i in range(n)),GRB.MINIMIZE)

'''
# Constraint 1: Each server must get the object from exactly one server
for i in range(n):
    m.addConstr(sum(x[k] for k in range(n) if network[i][k] != 0) == 1)
'''
# Constraint 2: Simplified since we only deal with one object and y_ijk is 1 - x_ij
# If object is taken from server k by server i, it cannot be stored on server i
for i in range(n):
    for k in range(n):
        if network[i][k] != 0:
            m.addConstr(x[i] + x[k] <= 1)

# Constraint 3 and 4: Already defined by the variable types (binary)

# Optimize model
m.optimize()

# Output results
#solution_x = {i: x[i].X for i in range(n)}
print("Optimized decision for x_i:")
for v in m.getVars():
    print(v)
