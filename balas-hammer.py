def compute_penalties(cost_matrix, active_rows, active_cols):
    penalties_rows = []
    penalties_cols = []

    # Rows
    for i in range(len(cost_matrix)):
        if not active_rows[i]:
            penalties_rows.append(-1)
            continue

        costs = [cost_matrix[i][j] for j in range(len(cost_matrix[0])) if active_cols[j]]
        costs.sort()

        if len(costs) >= 2:
            penalties_rows.append(costs[1] - costs[0])
        else:
            penalties_rows.append(0)

    # Columns
    for j in range(len(cost_matrix[0])):
        if not active_cols[j]:
            penalties_cols.append(-1)
            continue

        costs = [cost_matrix[i][j] for i in range(len(cost_matrix)) if active_rows[i]]
        costs.sort()

        if len(costs) >= 2:
            penalties_cols.append(costs[1] - costs[0])
        else:
            penalties_cols.append(0)

    return penalties_rows, penalties_cols


def bh(cost_matrix, provisions, demands):
    n = len(cost_matrix)
    m = len(cost_matrix[0])

    solution = [[0 for _ in range(m)] for _ in range(n)]

    active_rows = [True] * n
    active_cols = [True] * m

    while any(active_rows) and any(active_cols):
        penalties_rows, penalties_cols = compute_penalties(cost_matrix, active_rows, active_cols)

        max_row_penalty = max(penalties_rows)
        max_col_penalty = max(penalties_cols)

        if max_row_penalty >= max_col_penalty:
            i = penalties_rows.index(max_row_penalty)
            j = min(
                [j for j in range(m) if active_cols[j]],
                key=lambda j: cost_matrix[i][j]
            )
        else:
            j = penalties_cols.index(max_col_penalty)
            i = min(
                [i for i in range(n) if active_rows[i]],
                key=lambda i: cost_matrix[i][j]
            )

        x = min(provisions[i], demands[j])
        solution[i][j] = x

        provisions[i] -= x
        demands[j] -= x

        if provisions[i] == 0:
            active_rows[i] = False
        if demands[j] == 0:
            active_cols[j] = False

    return solution