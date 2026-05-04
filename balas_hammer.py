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

    solution = [[None for _ in range(m)] for _ in range(n)]

    active_rows = [True] * n
    active_cols = [True] * m

    while any(active_rows) and any(active_cols):
        penalties_rows, penalties_cols = compute_penalties(cost_matrix, active_rows, active_cols)

        max_row_penalty = max(penalties_rows)
        max_col_penalty = max(penalties_cols)

        # if max_row_penalty >= max_col_penalty:
        #     i = penalties_rows.index(max_row_penalty)
        #     j = min(
        #         [j for j in range(m) if active_cols[j]],
        #         key=lambda j: cost_matrix[i][j]
        #     )
        # else:
        #     j = penalties_cols.index(max_col_penalty)
        #     i = min(
        #         [i for i in range(n) if active_rows[i]],
        #         key=lambda i: cost_matrix[i][j]
        #     )

        if max_row_penalty > max_col_penalty:
            best_rows = [i for i, p in enumerate(penalties_rows) if p == max_row_penalty]
            i = min(best_rows, key=lambda i: min(cost_matrix[i][j] for j in range(m) if active_cols[j]))
            j = min((j for j in range(m) if active_cols[j]), key=lambda j: cost_matrix[i][j])

        elif max_col_penalty > max_row_penalty:
            best_cols = [j for j, p in enumerate(penalties_cols) if p == max_col_penalty]
            j = min(best_cols, key=lambda j: min(cost_matrix[i][j] for i in range(n) if active_rows[i]))
            i = min((i for i in range(n) if active_rows[i]), key=lambda i: cost_matrix[i][j])

        else:
            best_rows = [i for i, p in enumerate(penalties_rows) if p == max_row_penalty]
            best_cols = [j for j, p in enumerate(penalties_cols) if p == max_col_penalty]

            best_row = min(best_rows, key=lambda i: min(cost_matrix[i][j] for j in range(m) if active_cols[j]))
            best_col = min(best_cols, key=lambda j: min(cost_matrix[i][j] for i in range(n) if active_rows[i]))

            row_min = min(cost_matrix[best_row][j] for j in range(m) if active_cols[j])
            col_min = min(cost_matrix[i][best_col] for i in range(n) if active_rows[i])

            if row_min <= col_min:
                i = best_row
                j = min((j for j in range(m) if active_cols[j]), key=lambda j: cost_matrix[i][j])
            else:
                j = best_col
                i = min((i for i in range(n) if active_rows[i]), key=lambda i: cost_matrix[i][j])

        x = min(provisions[i], demands[j])
        solution[i][j] = x

        provisions[i] -= x
        demands[j] -= x

        if provisions[i] == 0 and demands[j] == 0:
            # Cell already allocated, but we need to signal degeneracy
            # Deactivate both — the allocated zero already recorded keeps basis count correct
            active_rows[i] = False
            active_cols[j] = False
            # If more iterations remain, inject an epsilon into the next available cell
            next_rows = [r for r in range(n) if active_rows[r]]
            next_cols = [c for c in range(m) if active_cols[c]]
            if next_rows and next_cols:
                solution[next_rows[0]][next_cols[0]] = 0  # epsilon basic cell
        elif provisions[i] == 0:
            active_rows[i] = False
        elif demands[j] == 0:
            active_cols[j] = False

    return solution