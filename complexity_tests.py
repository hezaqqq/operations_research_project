import time
from complexity import complexityTransportationProblems
from north_west import north_west
from balas_hammer import bh

def test():
    sizes = [10, 40]
    runs = 100

    print(f"{'n':>8} | {'North West (s)':>14} | {'Balas Hammer (s)':>16}")
    print("-" * 50)

    nw_file = open("complexity/nw_logs.txt", "w")
    bh_file = open("complexity/bh_logs.txt", "w")

    for n in sizes:
        nw_file.write(f"{n}\n")
        bh_file.write(f"{n}\n")

        total_nw = 0
        total_bh = 0

        for _ in range(runs):
            A, P, C = complexityTransportationProblems(n)

            start = time.perf_counter()
            north_west(P[:], C[:])
            end = time.perf_counter()
            duration_nw = end - start
            total_nw += duration_nw
            nw_file.write(f"{duration_nw}\n")

            start = time.perf_counter()
            bh(A, P[:], C[:])
            end = time.perf_counter()
            duration_bh = end - start
            total_bh += duration_bh
            bh_file.write(f"{duration_bh}\n")

        avg_nw = total_nw / runs
        avg_bh = total_bh / runs

        print(f"{n:8} | {avg_nw:14.6f} | {avg_bh:16.6f}")

        nw_file.write(f"AVG: {avg_nw}\n")
        bh_file.write(f"AVG: {avg_bh}\n")

    nw_file.close()
    bh_file.close()

if __name__ == "__main__":
    test()