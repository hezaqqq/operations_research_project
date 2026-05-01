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

    i = 0
    while i < len(path_start) and i < len(path_end) and path_start[i] == path_end[i]:
        i += 1

    return path_start[i - 1:] + path_end[i:][::-1]


def get_used_from_proposal(table):
    used = []
    for i in range(table.height):  # Lignes (Producteurs)
        for j in range(table.width):  # Colonnes (Clients)
            if table.proposal[i][j] is not None:
                used.append((i, j))
    return used


def cycle(table):
    n = table.height
    m = table.width

    used = get_used_from_proposal(table)

    # Création de la liste d'adjacence
    adj = {i: [] for i in range(n + m)}
    for r, c in used:
        u = r
        v = n + c
        adj[u].append(v)
        adj[v].append(u)

    visited = {}
    queue = deque()

    for i in range(n + m):
        if i not in visited:
            queue.append((i, -1))
            visited[i] = -1

            while queue:
                curr, parent = queue.popleft()

                for neighbor in adj[curr]:
                    if neighbor == parent:
                        continue

                    if neighbor in visited:
                        # Cycle trouvé
                        found_cycle = get_path(visited, curr, neighbor)

                        # Affichage pour debug
                        real_path = []
                        for node in found_cycle:
                            if node < n:
                                real_path.append(f"P{node + 1}")
                            else:
                                real_path.append(f"C{node - n + 1}")

                        print(f"Cycle détecté : {' -> '.join(real_path)}")
                        return True, found_cycle

                    visited[neighbor] = curr
                    queue.append((neighbor, curr))

    return False, None