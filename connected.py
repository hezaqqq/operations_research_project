def connected(n, m, used):

    adj = {i: [] for i in range(n + m)}
    for r, c in used:
        u, v = r, n + c
        adj[u].append(v)
        adj[v].append(u)

    total_nodes = n + m
    all_visited = set()
    sub_graphs = []

    for i in range(total_nodes):
        if i not in all_visited:

            current_subgraph = []
            queue = deque([i])
            visited = {i} #dans le BFS

            while queue:
                curr = queue.popleft()
                current_subgraph.append(curr)
                all_visited.add(curr)

                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            sub_graphs.append(current_subgraph)

    if len(sub_graphs) == 1:
        print("The graph is connected")
    else:
        print(f"The graph is not connected ({len(sub_graphs)} sub-graphs found.")
        for idx, sg in enumerate(sub_graphs):
            readable = []
            for node in sg:
                label = f"P{node + 1}" if node < n else f"C{node - n + 1}"
                readable.append(label)
            print(f" Sub-graph {idx + 1} : {', '.join(readable)}")

    return len(sub_graphs) == 1, sub_graphs

