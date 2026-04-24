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

data = read_txt('tables/tab_1.txt')

print(f"Dimensions: {data['n']} rows x {data['m']} columns")
print(f"Provisions (P): {data['P']}")
print(f"Orders (O): {data['O']}")
print("Cost Matrix (C):")
for row in data['C']:
    print(row)