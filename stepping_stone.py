from collections import deque
from cycle import get_used_from_proposal, cycle
from costs import marginal_cost

def compute_potentials(table):
    n = table.height
    m = table.width

    u = [None] * n
    v = [None] * m

    basic_cells = get_used_from_proposal(table)

    # degeneracy
    for start_i in range(n):
        if u[start_i] is not None:
            continue

        u[start_i] = 0

        changed = True
        while changed:
            changed = False

            for k in range(len(basic_cells)):
                i, j = basic_cells[k]

                # Compute v[j]
                if u[i] is not None and v[j] is None:
                    v[j] = table.costs[i][j] - u[i]
                    changed = True

                # Compute u[i]
                elif v[j] is not None and u[i] is None:
                    u[i] = table.costs[i][j] - v[j]
                    changed = True
    return u, v

def ensure_base_complete(table):
    n = table.height
    m = table.width

    while len(get_used_from_proposal(table)) < n + m - 1:
        empty_cells = []
        # get empty cells
        for r in range(n):
            for c in range(m):
                if table.proposal[r][c] is None:
                    cost = table.costs[r][c]
                    empty_cells.append((cost, r, c))

        # Sort by cost
        empty_cells.sort()

        for item in empty_cells:
            i, r, c = item

            table.proposal[r][c] = 0
            creates_cycle, i = cycle(table)

            if creates_cycle:
                table.proposal[r][c] = None
            else:
                break

def find_cycle_for_cell(start_row, start_col, table):
    available = get_used_from_proposal(table)
    available.append((start_row, start_col))

    queue = deque()
    queue.append((start_row, start_col, "row", [(start_row, start_col)]))

    while len(queue) > 0:
        r, c, direction, path = queue.popleft()

        candidates = []

        # Same row
        if direction == "row":
            for (nr, nc) in available:
                if nr == r and nc != c:
                    candidates.append((nr, nc))

        # Same column
        else:
            for (nr, nc) in available:
                if nc == c and nr != r:
                    candidates.append((nr, nc))

        # Alternate direction
        if direction == "row":
            next_direction = "col"
        else:
            next_direction = "row"

        for (nr, nc) in candidates:

            # Cycle found
            if nr == start_row and nc == start_col and len(path) >= 4:
                return path

            # Avoid revisiting
            already_in_path = False
            for (pr, pc) in path:
                if pr == nr and pc == nc:
                    already_in_path = True
                    break

            if not already_in_path:
                new_path = list(path)
                new_path.append((nr, nc))
                queue.append((nr, nc, next_direction, new_path))

    return None

def pivot(table, cycle_path):

    theta = None

    # Find minimum on negative positions
    for k in range(len(cycle_path)):
        if k % 2 == 1:
            r, c = cycle_path[k]
            val = table.proposal[r][c]

            if theta is None or val < theta:
                theta = val

    # Find leaving cell
    leaving_cell = None

    for k in range(len(cycle_path)):
        if k % 2 == 1:
            r, c = cycle_path[k]
            if table.proposal[r][c] == theta:
                leaving_cell = (r, c)
                break

    # Apply updates
    for k in range(len(cycle_path)):
        r, c = cycle_path[k]

        if table.proposal[r][c] is None:
            current = 0
        else:
            current = table.proposal[r][c]

        if k % 2 == 0:
            table.proposal[r][c] = current + theta
        else:
            table.proposal[r][c] = current - theta

    # Remove leaving cell
    r, c = leaving_cell
    table.proposal[r][c] = None

def stepping_stone(table):
    iteration = 0

    while True:
        iteration += 1

        n = table.height
        m = table.width

        basic_cells = get_used_from_proposal(table)
        base_size = len(basic_cells)

        if base_size < n + m - 1:
            ensure_base_complete(table)
            basic_cells = get_used_from_proposal(table)

        # Compute potentials
        u, v = compute_potentials(table)

        # Compute marginal costs
        marginals = marginal_cost(table.costs, [
            [u[i] + v[j] for j in range(m)]
            for i in range(n)
        ])

        # Find entering path
        best_path = None
        best_marginal = 0

        for i in range(n):
            for j in range(m):

                if table.proposal[i][j] is not None:
                    continue

                val = marginals[i][j]

                if val < best_marginal:
                    cycle_path = find_cycle_for_cell(i, j, table)

                    if cycle_path is not None:
                        best_marginal = val
                        best_path = (i, j, cycle_path)

        if best_path is None:
            break

        i_in, j_in, cycle_path = best_path

        pivot(table, cycle_path)