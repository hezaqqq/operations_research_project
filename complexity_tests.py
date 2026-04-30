import time
from complexity import complexityTransportationProblems
from north_west import north_west
from balas_hammer import bh

def test():
    sizes = [10, 40, 10**2, 4*10**2, 10**3, 4*10**3, 10**4]
    runs = 100

    print(f"{'n':>8} | {'North West (s)':>12} | {'Balas Hammer (s)':>12}")
    print("-" * 45)

    for n in sizes:
        total_nw = 0
        total_bh = 0

        for i in range(runs):
            A, P, C = complexityTransportationProblems(n)

            start = time.perf_counter()
            north_west(P[:], C[:])
            end = time.perf_counter() # time.clock() doesn't exist anymore
            total_nw += (end - start)

            start = time.perf_counter()
            bh(A, P[:], C[:])
            end = time.perf_counter()
            total_bh += (end - start)

        avg_nw = total_nw / runs
        avg_bh = total_bh / runs

        print(f"{n:8} | {avg_nw:14.6f} | {avg_bh:16.6f}")

if __name__ == "__main__":
    test()