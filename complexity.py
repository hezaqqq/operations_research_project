import random

import random

def complexityTransportationProblems(n):
    # Matrix A
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            value = random.randint(1, 100)
            row.append(value)
        A.append(row)

    # Temp matrix
    temp = []
    for i in range(n):
        row = []
        for j in range(n):
            value = random.randint(1, 100)
            row.append(value)
        temp.append(row)

    # P: sum of each row in temp
    P = []
    for i in range(n):
        row_sum = 0
        for j in range(n):
            row_sum += temp[i][j]
        P.append(row_sum)

    # C: sum of each column in temp
    C = []
    for j in range(n):
        col_sum = 0
        for i in range(n):
            col_sum += temp[i][j]
        C.append(col_sum)

    return A, P, C

def writeTransportToFile(n, filename="tables/tab_complexity.txt"):
    A, P, C = complexityTransportationProblems(n)

    with open(filename, "w") as f:
        f.write(f"{n} {n}\n")

        # A[i] + P[i]
        for i in range(n):
            row = " ".join(map(str, A[i]))
            f.write(f"{row} {P[i]}\n")

        f.write(" ".join(map(str, C)) + "\n")

    return A, P, C