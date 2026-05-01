def north_west(provisions, demands):
    n = len(provisions)
    m = len(demands)

    # on met la matrice solution à 0
    solution = [[None for _ in range(m)] for _ in range(n)]

    i, j = 0, 0

    while i < n and j < m:
        x = min(provisions[i], demands[j])
        solution[i][j] = x

        provisions[i] -= x
        demands[j] -= x

        # si une ligne est épuisée (le fournisseur à plus rienà donner), on passe à la suivante
        if provisions[i] == 0 and i < n - 1:
            i += 1

        # si une colonne est épuisée (le client a plus besoin de rien), on passe à la suivante
        elif demands[j] == 0:
            j += 1

    return solution