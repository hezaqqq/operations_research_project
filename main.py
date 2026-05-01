from north_west import north_west
from balas_hammer import bh
from complexity import writeTransportToFile

class ConstraintTable:
    def __init__(self, width: int, height: int, costs: list[list[int]], provisions: list[int], orders: list[int], proposal: list[list[int]] | None = None):
        self.width = width
        self.height = height
        self.costs = costs
        self.provisions = provisions
        self.orders = orders

        self.proposal = proposal

    def is_equilibrium(self) -> bool:
        return sum(self.orders) == sum(self.provisions)

    def equilibrate(self):
        total_orders = sum(self.orders)
        total_provisions = sum(self.provisions)

        # add fake customer (add column)
        if total_orders < total_provisions:
            new_col_orders = total_provisions - total_orders

            for row in range(self.height):
                self.costs[row].append(0)

            self.orders.append(new_col_orders)
            self.width += 1

        # add fake supplier (add row)
        elif total_provisions < total_orders:
            new_row_provisions = total_orders - total_provisions

            self.costs.append([0] * self.width)
            self.provisions.append(new_row_provisions)
            self.height += 1

        # (it the provisions and orders are the same, we are at equilibrium, so don't do anything)


    def proposal_cost(self) -> float:
        if self.proposal is None:
            return 0.0

        result = 0

        for y in range(self.height):
            for x in range(self.width):
                result += self.costs[y][x] * self.proposal[y][x]

        return result


    def display_costs(self):
        print("Cost matrix :")
        for row in self.costs:
            for x in row:
                print(f"{x:4}", end=" ")
            print()
        print()
        print("----------------")


    def display_proposal(self):
        print("Proposal :")
        y = 0
        for row in self.proposal:
            for x in row:
                print(f"{x:4}", end=" ")

            print(f"  | {self.provisions[y]:4}  ")
            y += 1

        for x in self.proposal[0]:
            print(".....", end="")
        print()

        for x in self.orders:
            print(f"{x:4}", end=" ")
        print()
        print()
        print("----------------")


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

    return ConstraintTable(m, n, cost_matrix, provisions, orders)


def compute_potentials(data: ConstraintTable, basic):
    costs = data.costs
    u = [None] * data.width
    v = [None] * data.height

    u[0] = 0

    changed = True
    while changed:
        changed = False

        for i, j in basic:
            if u[i] is not None and v[j] is None:
                v[j] = costs[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = costs[i][j] - v[j]
                changed = True

    return u, v


def main():
    data = None

    while data is None:
        print("\nWhat type of transportation problem do you want to use?")
        print("1. Pre-made transportation problems")
        print("2. Generate random problems (complexity study)")
        user_in = input("> ")
        print("")
        if user_in == "1":

            table_name = input("Enter problem number (1-12) > ")
            try:
                data = read_txt("tables/tab_" + str(table_name) + ".txt")

            except FileNotFoundError:
                print("Invalid problem number")

        elif user_in == "2":
            size = input("Enter the size of the table (n): ")

            try:
                size = int(size)
                writeTransportToFile(size)
                data = read_txt("tables/tab_complexity.txt")
                table_name = "complexity"
            except ValueError:
                print("Enter a valid integer")

    print("\n tab_" + str(table_name) + ".txt")
    # Print cost matrix with provisions
    for i, row in enumerate(data.costs):
        for x in row:
            print(f"{x:4}", end=" ")

        print(f" | {data.provisions[i]:4}")

    print("-----" * len(data.orders))
    for x in data.orders:
        print(f"{x:4}", end=" ")

    print("\n")

    data.display_costs()

    if data.is_equilibrium():
        print("Equilibrium")
    else:
        print("Not Equilibrium")
        data.equilibrate()
        print("Adjusted to:")
        data.display_costs()

    print("Which algorithm would you like to use to fix the initial proposal?")
    print("1: North-West")
    print("2: Balas-Hammer")
    user_in = input("> ")

    if user_in == "1":
        data.proposal = north_west(data.provisions[:], data.orders[:])
        data.display_proposal()
    elif user_in == "2":
        data.proposal = bh(data.costs, data.provisions[:], data.orders[:])
        data.display_proposal()

    print(f"Current cost: {data.proposal_cost()}")


if __name__ == "__main__":
    main()

