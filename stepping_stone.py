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
                print(f"[Degeneracy] Added degenerate cell: (P{r+1}, C{c+1}) = 0")
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

    print(f"[Pivot] Pivot={theta}, leaving cell: (P{leaving_cell[0]+1}, C{leaving_cell[1]+1})")

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

def display_proposal(table):
    n = table.height
    m = table.width
    col_w = 8

    print("\nTransport proposal:")
    print("-" * (col_w * (m + 2)))

    header = "".center(col_w)

    for j in range(m):
        header += f"C{j+1}".center(col_w)

    header += "Supply".center(col_w)

    print(header)
    print("-" * (col_w * (m + 2)))

    for i in range(n):
        row = f"P{i+1}".center(col_w)

        for j in range(m):
            val = table.proposal[i][j]
            if val is None:
                row += "-".center(col_w)
            else:
                row += str(val).center(col_w)

        row += str(table.provisions[i]).center(col_w)
        print(row)

    print("-" * (col_w * (m + 2)))

    demand_row = "Demand".center(col_w)
    for j in range(m):
        demand_row += str(table.orders[j]).center(col_w)

    print(demand_row)
    print("-" * (col_w * (m + 2)))

def display_cost_table(table, u, v, marginals):
    n = table.height
    m = table.width
    col_w = 10

    print("\nPotential costs and marginal costs:")
    print("-" * (col_w * (m + 1) * 2 + 6))

    header = "".center(col_w)

    for j in range(m):
        header += f"C{j + 1}(pot)".center(col_w)

    header += "  |  "

    for j in range(m):
        header += f"C{j + 1}(marg)".center(col_w)

    print(header)
    print("-" * (col_w * (m + 1) * 2 + 6))

    for i in range(n):
        row = f"P{i + 1}".center(col_w)

        # Potential (u_i + v_j)
        for j in range(m):
            val = u[i] + v[j]
            # Removed marker logic here
            row += str(val).center(col_w)

        row += "  |  "

        # Marginal (Actual Cost - Potential)
        for j in range(m):
            val = marginals[i][j]
            # Removed marker logic here
            row += str(val).center(col_w)
        print(row)

    print("-" * (col_w * (m + 1) * 2 + 6))

def stepping_stone(table):
    iteration = 0

    while True:
        iteration += 1
        print(f"Iteration {iteration}")

        n = table.height
        m = table.width

        basic_cells = get_used_from_proposal(table)
        base_size = len(basic_cells)

        if base_size < n + m - 1:
            print(f"\n[Degeneracy] Incomplete basis: {base_size} cells (expected {n+m-1})")
            ensure_base_complete(table)
            basic_cells = get_used_from_proposal(table)
            print(f"[Degeneracy] Basis completed: {len(basic_cells)} cells")
        else:
            print(f"\n[Basis] {base_size} basic cells non-degenerate proposal")

        # Compute potentials
        u, v = compute_potentials(table)

        # Compute marginal costs
        marginals = marginal_cost(table.costs, [
            [u[i] + v[j] for j in range(m)]
            for i in range(n)
        ])

        display_cost_table(table, u, v, marginals)

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
            print("\nAll marginal costs >= 0: optimal solution reached.")
            break

        i_in, j_in, cycle_path = best_path

        print(f"\n[Path] (P{i_in+1}, C{j_in+1}), marginal cost = {best_marginal}")

        labels = []
        for k in range(len(cycle_path)):
            r, c = cycle_path[k]
            sign = "+" if k % 2 == 0 else "-"
            labels.append(f"{sign}(P{r+1},C{c+1})")

        print("Cycle: " + " -> ".join(labels))

        pivot(table, cycle_path)

    print("\n" + "-" * 70)
    print("Optimal Solution:")
    display_proposal(table)
    print(f"\nMinimum transport cost: {table.proposal_cost()}")
    print("-" * 70 + "\n")