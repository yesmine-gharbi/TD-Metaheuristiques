
# Matrice des couts
couts = [
    [5, 3, 4],
    [6, 7, 2]
]

# Solution initiale
solution = [
    [0, 0, 8],
    [4, 5, 0]
]

# Calcul du cout total
def calculer_cout(s):
    total = 0

    for i in range(2):
        for j in range(3):
            total += s[i][j] * couts[i][j]

    return total


# Generer les voisins
def voisins(s):
    liste = []

    for i in range(3):
        for j in range(3):

            if i != j and s[0][i] > 0 and s[1][j] > 0:

                nouveau = [s[0].copy(), s[1].copy()]

                nouveau[0][i] -= 1
                nouveau[0][j] += 1

                nouveau[1][i] += 1
                nouveau[1][j] -= 1

                liste.append(nouveau)

    return liste


# Recherche taboue
meilleure = [solution[0].copy(), solution[1].copy()]

taboue = []

for iteration in range(20):

    liste = voisins(solution)

    meilleur_voisin = None
    meilleur_cout = float('inf')

    for v in liste:

        if v not in taboue:

            cout = calculer_cout(v)

            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleur_voisin = v

    if meilleur_voisin is None:
        break

    solution = meilleur_voisin

    taboue.append(solution)

    if len(taboue) > 3:
        taboue.pop(0)

    if calculer_cout(solution) < calculer_cout(meilleure):
        meilleure = [solution[0].copy(), solution[1].copy()]

    print("Iteration :", iteration + 1)
    print("Solution :", solution)
    print("Cout :", calculer_cout(solution))


print("\nMeilleure solution :")
print(meilleure)

print("Cout minimal :", calculer_cout(meilleure))