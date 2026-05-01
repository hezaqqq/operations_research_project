import numpy as np

def potential_marginal(quantity_matrix, cost_matrix):
    # we need to find all the routes that have provisions and their respective cost
    considered_routes = []
    linsysoffset = len(quantity_matrix)
    n_vars = len(quantity_matrix) + len(quantity_matrix[0])

    for i in range(len(quantity_matrix)):
        for j in range(len(quantity_matrix[0])):
            if quantity_matrix[i][j] > 0:
                considered_routes.append((i, j + linsysoffset, cost_matrix[i][j]))

    print("Considered routes:", considered_routes)

    # then we need to make the linear system and solve it to get the real values of E()
    temp_arr1 = [[0] * n_vars for _ in range(n_vars)]
    temp_arr2 = []

    for i in range(len(considered_routes)):
        temp_arr1[i][considered_routes[i][0]] = 1
        temp_arr1[i][considered_routes[i][1]] = -1
        temp_arr2.append(considered_routes[i][2])

    # Last equation: fix the reference potential E(S2) = 0 (index 1 here)
    temp_arr1[-1] = [0] * n_vars
    temp_arr1[-1][1] = 1   # E(S2) = 0 as in the course example
    temp_arr2.append(0)

    a = np.array(temp_arr1)
    b = np.array(temp_arr2)
    x = np.linalg.solve(a, b) # this should contain the E()s of the sources then the customers

    # now we can compute the potential costs matrix
    potentials = [[0] * len(quantity_matrix[0]) for _ in range(len(quantity_matrix))]
    marginals = [[0] * len(quantity_matrix[0]) for _ in range(len(quantity_matrix))]

    for i in range(len(quantity_matrix)):
        for j in range(len(quantity_matrix[0])):
            potentials[i][j] = round(x[i] - x[j + linsysoffset])
            marginals[i][j] = cost_matrix[i][j] - potentials[i][j]
    return potentials, marginals


provision = [[25, 0, 0], [10, 15, 0], [0, 5, 20]]
cost = [[5, 7, 8], [6, 8, 5], [6, 7, 7]]

potential, marginal = potential_marginal(provision, cost)
print("Potential cost table:")
for row in potential:
    print(row)
print("Marginal cost table:")
for row in marginal:
    print(row)