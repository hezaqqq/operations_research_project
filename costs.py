import numpy as np

def potential_cost(quantity_matrix, cost_matrix):
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

    for i in range(len(quantity_matrix)):
        for j in range(len(quantity_matrix[0])):
            potentials[i][j] = round(x[i] - x[j + linsysoffset])

    return potentials


def marginal_cost(cost_matrix, potential_cost):
    marginals = [[0] * len(cost_matrix[0]) for _ in range(len(cost_matrix))]

    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            marginals[i][j] = cost_matrix[i][j] - potential_cost[i][j]

    return marginals


def display_potential(potential_table):
    n_sources = len(potential_table)
    n_clients = len(potential_table[0])
    col_width = 14

    header = "Potential cost"
    for j in range(n_clients):
        header += f"C{j+1}".center(col_width)

    print()
    print(header)
    print("-" * (col_width * (n_clients + 1)))

    for i in range(n_sources):
        row = f"S{i+1}".center(col_width)

        for j in range(n_clients):
            cell = f"{potential_table[i][j]}"
            row += cell.center(col_width)
        print(row)

    print("-" * (col_width * (n_clients + 1)))


def display_marginal(marginal_table):
    n_sources = len(marginal_table)
    n_clients = len(marginal_table[0])
    col_width = 14

    header = "Marginal cost"
    for j in range(n_clients):
        header += f"C{j+1}".center(col_width)

    print()
    print(header)
    print("-" * (col_width * (n_clients + 1)))

    for i in range(n_sources):
        row = f"S{i+1}".center(col_width)

        for j in range(n_clients):
            cell = f"{marginal_table[i][j]}"
            row += cell.center(col_width)
        print(row)

    print("-" * (col_width * (n_clients + 1)))


provision = [[25, 0, 0], [10, 15, 0], [0, 5, 20]]
cost = [[5, 7, 8], [6, 8, 5], [6, 7, 7]]

potential = potential_cost(provision, cost)
marginal = marginal_cost(cost, potential)

display_potential(potential)
display_marginal(marginal)