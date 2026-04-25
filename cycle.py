from collections import deque


def get_path(parent_dict, start, end):
    path_start = []
    curr = start
    while curr != -1:
        path_start.append(curr)
        curr = parent_dict[curr]

    path_end = []
    curr = end
    while curr != -1:
        path_end.append(curr)
        curr = parent_dict[curr]

    path_start.reverse()
    path_end.reverse()

    i=0
    while i < len(path_start) and i < len(path_end) and path_start[i] == path_end[i]:
        i += 1

    return path_start[i-1:] + path_end[i:][::-1]


def cycle_test(filename, used):
    with open(filename, 'r') as f:
        first_line = f.readline().split()
        n = int(first_line[0])
        m = int(first_line[1])

    # adhency mat
    adj = {i: [] for i in range(n + m)}
    for r, c in used:
        u = r
        v = n + c
        adj[u].append(v)
        adj[v].append(u)

    # BFS pour trouver si on a un cycle
    visited = {}
    queue = deque()

    for i in range(n + m):
        if i not in visited:
            queue.append((i, -1))
            visited[i] = -1

            while queue:
                item = queue.popleft()
                curr = item[0]
                parent = item[1]

                for neighbor in adj[curr]:
                    if neighbor == parent:
                        continue

                    if neighbor in visited:
                    # on a donc ici le cycle qui est détecté et on va essayer de redonner le chemin
                        cycle = get_path(visited, curr, neighbor)

                        print(f"We have a cycle !\nPath : {cycle}")   #ici on a le cycle classique. aux  index impair on fait + 1 pour trouver la bon producer et pour les pairs on fait index - n pour trouver le customer

                    # Ici on a sous forme de customer et producteur
                        real_path = []
                        for node in cycle:
                            if node < n:
                                real_path.append(f"P{node + 1}")
                            else:
                                real_path.append(f"C{node - n + 1}")
                        print("Real physical path :", " -> ".join(real_path))

                        return True, cycle

                    visited[neighbor] = curr
                    queue.append((neighbor, curr))

    print("No cycle found -> Acyclic")
    return False


# Exemple aveec le graph exemple du cours pas avec un des 12 graphs (à ne pas garder, c'était pour voir comment ça amrche)
with_cycle = [(0, 0), (0, 1), (1, 1), (1, 0)]
without_cycle = [(0, 0), (0, 1), (1, 1)]

print("Si on a un cycle -->")
cycle_test('Tab1.txt', with_cycle)

print("\nSi on n'a pas de cycle -->")
cycle_test('Tab1.txt', without_cycle)
