from north_west import north_west
from balas_hammer import bh
from complexity import writeTransportToFile
from stepping_stone import stepping_stone

class ConstraintTable:
    def __init__(self, width: int, height: int, costs: list[list[int]],
                 provisions: list[int], orders: list[int],
                 proposal: list[list[int]] | None = None):
        self.width = width
        self.height = height
        self.costs = costs
        self.provisions = provisions
        self.orders = orders
        self.proposal = proposal

    def is_equilibrium(self) -> bool:
        return sum(self.orders) == sum(self.provisions)

    def equilibrate(self):
        total_supply = sum(self.provisions)
        total_demand = sum(self.orders)

        if total_demand < total_supply:
            # Add a dummy customer (new column with zero cost)
            surplus = total_supply - total_demand
            for row in self.costs:
                row.append(0)
            self.orders.append(surplus)
            self.width += 1

        elif total_supply < total_demand:
            # Add a dummy supplier (new row with zero cost)
            surplus = total_demand - total_supply
            self.costs.append([0] * self.width)
            self.provisions.append(surplus)
            self.height += 1

    def proposal_cost(self) -> float:
        if self.proposal is None:
            return 0.0
        return sum(
            self.costs[i][j] * (self.proposal[i][j] if self.proposal[i][j] is not None else 0)
            for i in range(self.height)
            for j in range(self.width)
        )

    def display_constraint_table(self):
        col_w = 6
        sep = "-" * (col_w * (self.width + 2))

        print("\nConstraint table:")
        print(sep)

        # Header
        header = "".center(col_w)
        header += "".join(f"C{j+1}".center(col_w) for j in range(self.width))
        header += "Supply".center(col_w)
        print(header)
        print(sep)

        # Rows
        for i in range(self.height):
            row =f"P{i+1}".center(col_w)
            row += "".join(str(self.costs[i][j]).center(col_w) for j in range(self.width))
            row += str(self.provisions[i]).center(col_w)
            print(row)

        print(sep)

        # Demand row
        demand_row = "Demand".center(col_w)
        demand_row += "".join(str(self.orders[j]).center(col_w) for j in range(self.width))
        print(demand_row)
        print( sep)

    def display_proposal(self):
        col_w = 8
        sep = "-" * (col_w * (self.width + 2))

        print("\nInitial transport proposal:")
        print(sep)

        header = "".center(col_w)
        header += "".join(f"C{j+1}".center(col_w) for j in range(self.width))
        header += "Supply".center(col_w)
        print(header)
        print(sep)

        for i in range(self.height):
            row = f"P{i+1}".center(col_w)
            row += "".join(
                (str(self.proposal[i][j]) if self.proposal[i][j] is not None else "-").center(col_w)
                for j in range(self.width)
            )
            row += str(self.provisions[i]).center(col_w)
            print(row)

        print(sep)
        demand_row = "Demand".center(col_w)
        demand_row += "".join(str(self.orders[j]).center(col_w) for j in range(self.width))
        print(demand_row)
        print(sep)

def read_txt(filename: str) -> ConstraintTable:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n, m = map(int, lines[0].split())

    costs = []
    provisions = []
    for i in range(1, 1 + n):
        values = list(map(int, lines[i].split()))
        costs.append(values[:m])
        provisions.append(values[m])

    orders = list(map(int, lines[1 + n].split()))

    return ConstraintTable(m, n, costs, provisions, orders)

def load_problem() -> tuple[ConstraintTable, str]:
    while True:
        print("What type of transportation problem do you want to use?")
        print("1. Pre-made problems (1–12)")
        print("2. Generate a random problem (complexity study)")
        choice = input("  > ").strip()

        if choice == "1":
            number = input("Enter problem number (1–12): ").strip()
            filename = f"tables/tab_{number}.txt"
            try:
                return read_txt(filename), number
            except FileNotFoundError:
                print(f"File not found: {filename}")

        elif choice == "2":
            size_str = input("Enter table size (n): ").strip()
            try:
                size = int(size_str)
                writeTransportToFile(size)
                return read_txt("tables/tab_complexity.txt"), f"complexity ({size}x{size})"
            except ValueError:
                print("Please enter a valid integer.")
            except FileNotFoundError:
                print("Could not read generated file.")
        else:
            print("Please enter 1 or 2.")


def choose_initial_algorithm(data: ConstraintTable):
    while True:
        print("\nWhich algorithm should be used to build the initial proposal?")
        print("1. North-West")
        print("2. Balas-Hammer")
        choice = input("  > ").strip()

        if choice == "1":
            data.proposal = north_west(data.provisions[:], data.orders[:])
            print("\n[North-West] Initial proposal built.")
            data.display_proposal()
            print(f"\nInitial transport cost: {data.proposal_cost()}")
            return

        elif choice == "2":
            data.proposal = bh(data.costs, data.provisions[:], data.orders[:])
            print("\n[Balas-Hammer] Initial proposal built.")
            data.display_proposal()
            print(f"\nInitial transport cost: {data.proposal_cost()}")
            return

        else:
            print("Please enter 1 or 2.")

def main():
    run_another = True

    while run_another:

        data, label = load_problem()
        print("tab_" + str(label) + ".txt")

        data.display_constraint_table()

        if data.is_equilibrium():
            print("\n[Equilibrium] Supply equals demand")
        else:
            total_s = sum(data.provisions)
            total_d = sum(data.orders)
            print(f"\n[Not balanced] Supply={total_s}, Demand={total_d} — adding dummy {'customer' if total_d < total_s else 'supplier'}...")
            data.equilibrate()
            print("Adjusted constraint table:")
            data.display_constraint_table()

        choose_initial_algorithm(data)

        print(f"\n{'-'*70}")
        print("Stepping-stone method with potentials")
        stepping_stone(data)

        print("\n Would you like to solve another transportation problem?")
        print("1. Yes")
        print("2. No")
        again = input("  > ").strip()
        print()
        run_another = (again == "1")

if __name__ == "__main__":
    main()