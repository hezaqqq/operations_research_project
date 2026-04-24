def read_txt(filename):
    with open(filename, 'r') as file:
        lines = []
        for line in file:
            stripped = line.strip()
            if stripped:
                lines.append(stripped)

    first_line = lines[0].split()
    n = int(first_line[0])
    m = int(first_line[1])

    cost_matrix = []
    provisions = []

    for i in range(1, 1 + n):
        row_values = list(map(int, lines[i].split()))
        costs = row_values[:m]
        provision = row_values[m]

        cost_matrix.append(costs)
        provisions.append(provision)

    orders = list(map(int, lines[1 + n].split()))

    return {
        "n": n,
        "m": m,
        "C": cost_matrix,
        "P": provisions,
        "O": orders
    }

def compute_potentials(C, basic):
    n = len(C)
    m = len(C[0])

    u = [None] * n
    v = [None] * m

    u[0] = 0

    changed = True
    while changed:
        changed = False

        for i, j in basic:
            if u[i] is not None and v[j] is None:
                v[j] = C[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = C[i][j] - v[j]
                changed = True

    return u, v


def display(data):
    print("Cost matrix :")
    for row in data["C"]:
        for x in row:
            print(f"{x:4}", end=" ")
        print()
    print()
    print("----------------")


data = read_txt('tables/tab_12.txt')
display(data)