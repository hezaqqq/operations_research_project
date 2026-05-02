import time
from complexity import complexityTransportationProblems
from north_west import north_west
from balas_hammer import bh
from stepping_stone import stepping_stone


class TransportationTable:
    def __init__(self, costs, provisions, orders, proposal):
        self.costs = costs
        self.provisions = provisions
        self.orders = orders
        self.proposal = proposal
        self.height = len(provisions)
        self.width = len(orders)

    def proposal_cost(self):
        total = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.proposal[i][j] is not None:
                    total += self.proposal[i][j] * self.costs[i][j]
        return total


def test():
    # Matrix sizes to test
    sizes = [10, 40, 10**2, 4*10**2, 10**3, 4*10**3, 10**4]
    runs = 100


    # Ensure the 'complexity' directory exists or change the path below
    try:
        log_file = open("complexity/full_stepping_stone_bench.txt", "w")
    except FileNotFoundError:
        log_file = open("full_stepping_stone_bench.txt", "w")

    for n in sizes:
        log_file.write(f"--- N = {n} ---\n")
        log_file.write("Run | tNW(n) | tBH(n) | (thetaNW + tNW) | (thetaBH + tBH)\n")

        sums = {"tNW": 0, "tBH": 0, "totalNW": 0, "totalBH": 0}

        for r in range(runs):
            A, P, C = complexityTransportationProblems(n)

            # --- NORTH WEST METRICS ---
            start_theta_nw = time.perf_counter()
            init_nw = north_west(P[:], C[:])
            theta_nw = time.perf_counter() - start_theta_nw

            table_nw = TransportationTable(A, P[:], C[:], init_nw)
            start_t_nw = time.perf_counter()
            stepping_stone(table_nw)
            t_nw = time.perf_counter() - start_t_nw

            # --- BALAS HAMMER METRICS ---
            start_theta_bh = time.perf_counter()
            init_bh = bh(A, P[:], C[:])
            theta_bh = time.perf_counter() - start_theta_bh

            table_bh = TransportationTable(A, P[:], C[:], init_bh)
            start_t_bh = time.perf_counter()
            stepping_stone(table_bh)
            t_bh = time.perf_counter() - start_t_bh

            # Calculate Totals
            total_nw = theta_nw + t_nw
            total_bh = theta_bh + t_bh

            # Record Individual Values
            log_file.write(f"{r + 1:3} | {t_nw:.6f} | {t_bh:.6f} | {total_nw:.6f} | {total_bh:.6f}\n")

            # Update Sums
            sums["tNW"] += t_nw
            sums["tBH"] += t_bh
            sums["totalNW"] += total_nw
            sums["totalBH"] += total_bh

        # Log Averages
        avg_t_nw = sums["tNW"] / runs
        avg_t_bh = sums["tBH"] / runs
        avg_tot_nw = sums["totalNW"] / runs
        avg_tot_bh = sums["totalBH"] / runs

        log_file.write(f"AVG | {avg_t_nw:.6f} | {avg_t_bh:.6f} | {avg_tot_nw:.6f} | {avg_tot_bh:.6f}\n\n")
        print(f"Completed N={n}")

    log_file.close()


if __name__ == "__main__":
    test()