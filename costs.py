from cycle import get_used_from_proposal


def compute_potentials(table):
    n = table.height
    m = table.width

    u = [None] * n   # u = potentials for sources (rows)
    v = [None] * m  # v = potentials for clients (columns)

    basic_cells = get_used_from_proposal(table)

    # we repeat the process until all potentials are computed
    for start_i in range(n):

        # Skip if already computed
        if u[start_i] is not None:
            continue
        u[start_i] = 0

        changed = True

        while changed:
            changed = False

            for k in range(len(basic_cells)):
                i, j = basic_cells[k]

                # If u[i] is known, compute v[j]
                if u[i] is not None and v[j] is None:
                    v[j] = table.costs[i][j] - u[i]
                    changed = True

                # If v[j] is known, compute u[i]
                elif v[j] is not None and u[i] is None:
                    u[i] = table.costs[i][j] - v[j]
                    changed = True

    return u, v


def build_potential_matrix(u, v):
    n = len(u)
    m = len(v)

    potential = []

    # Build matrix: potential[i][j] = u[i] + v[j]
    for i in range(n):
        row = []

        for j in range(m):
            value = u[i] + v[j]
            row.append(value)

        potential.append(row)

    return potential


def marginal_cost(cost_matrix, potential_matrix):
    n = len(cost_matrix)
    m = len(cost_matrix[0])

    marginals = []

    # marginal[i][j] = cost[i][j] - potential[i][j]
    for i in range(n):
        row = []

        for j in range(m):
            value = cost_matrix[i][j] - potential_matrix[i][j]
            row.append(value)

        marginals.append(row)

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

    # Display each row
    for i in range(n_sources):
        row = f"S{i+1}".center(col_width)

        for j in range(n_clients):
            cell = str(potential_table[i][j])
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

    # Display each row
    for i in range(n_sources):
        row = f"S{i+1}".center(col_width)

        for j in range(n_clients):
            cell = str(marginal_table[i][j])
            row += cell.center(col_width)

        print(row)

    print("-" * (col_width * (n_clients + 1)))