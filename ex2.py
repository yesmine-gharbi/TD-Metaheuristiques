
from collections import deque
from itertools import product

# ==========================================
# 1. DONNEES DU PROBLEME
# ==========================================

cout = [
    [5, 3, 4],
    [6, 7, 2]
]

stock = [8, 9]
demande = [4, 5, 8]

m = len(stock)
n = len(demande)

assert sum(stock) == sum(demande), \
    "Le probleme n'est pas equilibre."


# ==========================================
# 2. CALCUL DU COUT TOTAL
# ==========================================

def f(x):
    total = 0

    for i in range(m):
        for j in range(n):
            total += cout[i][j] * x[i][j]

    return total


# ==========================================
# 3. SOLUTION INITIALE
# ==========================================

def solution_initiale():
    s = stock[:]
    d = demande[:]

    x = [[0] * n for _ in range(m)]

    i = 0
    j = 0

    while i < m and j < n:
        q = min(s[i], d[j])

        x[i][j] = q
        s[i] -= q
        d[j] -= q

        if s[i] == 0:
            i += 1

        if d[j] == 0:
            j += 1

    return x


# ==========================================
# 4. GENERATION DES VOISINS
# ==========================================

def voisins(x):
    resultat = []

    for a in range(n):
        for b in range(n):

            if a == b:
                continue

            # Verifier que le mouvement est possible
            if x[0][a] >= 1 and x[1][b] >= 1:

                y = [ligne[:] for ligne in x]

                # Modification des livraisons de D1
                y[0][a] -= 1
                y[0][b] += 1

                # Compensation par D2
                y[1][a] += 1
                y[1][b] -= 1

                resultat.append(y)

    return resultat


# ==========================================
# 5. CLE D'UNE SOLUTION
# ==========================================

def cle(x):
    return tuple(tuple(ligne) for ligne in x)


# ==========================================
# 6. RECHERCHE TABOUE
# ==========================================

def recherche_tabou(
    nb_iter=100,
    taille_tabou=7,
    stagnation_max=15
):
    s = solution_initiale()

    meilleur = [ligne[:] for ligne in s]
    meilleur_cout = f(s)

    liste_taboue = deque(maxlen=taille_tabou)
    liste_taboue.append(cle(s))

    stagnation = 0

    print("Solution initiale :", s)
    print("Cout initial :", f(s))

    for iteration in range(1, nb_iter + 1):

        candidats = [
            v for v in voisins(s)
            if cle(v) not in liste_taboue
            or f(v) < meilleur_cout
        ]

        if not candidats:
            print("Aucun voisin autorise. Arret.")
            break

        # Choisir le voisin ayant le cout minimal
        s = min(candidats, key=f)
        liste_taboue.append(cle(s))

        cout_courant = f(s)

        # Mise a jour de la meilleure solution
        if cout_courant < meilleur_cout:
            meilleur = [ligne[:] for ligne in s]
            meilleur_cout = cout_courant
            stagnation = 0
        else:
            stagnation += 1

        print(
            f"Iteration {iteration:3d} : "
            f"cout courant = {cout_courant:3d} | "
            f"meilleur cout = {meilleur_cout}"
        )

        if stagnation >= stagnation_max:
            print("Stagnation : arret.")
            break

    return meilleur, meilleur_cout


# ==========================================
# 7. VERIFICATION EXACTE
# ==========================================

def verification_exacte():
    meilleur = None
    meilleur_cout = float("inf")

    # Enumerer les quantites envoyees par D1
    for x11, x12, x13 in product(
        range(demande[0] + 1),
        range(demande[1] + 1),
        range(demande[2] + 1)
    ):

        # D1 doit utiliser exactement ses 8 containers
        if x11 + x12 + x13 != stock[0]:
            continue

        # D2 satisfait les demandes restantes
        x21 = demande[0] - x11
        x22 = demande[1] - x12
        x23 = demande[2] - x13

        x = [
            [x11, x12, x13],
            [x21, x22, x23]
        ]

        cout_actuel = f(x)

        if cout_actuel < meilleur_cout:
            meilleur = [ligne[:] for ligne in x]
            meilleur_cout = cout_actuel

    return meilleur, meilleur_cout


# ==========================================
# 8. AFFICHAGE DES RESULTATS
# ==========================================

def afficher_solution(titre, x, cout_total):
    print("\n" + titre)

    print("        M1  M2  M3")

    for i in range(m):
        print(
            f"D{i + 1} :   "
            + "   ".join(str(q) for q in x[i])
        )

    print("\nDetails des livraisons :")

    for i in range(m):
        for j in range(n):
            print(
                f"D{i + 1} -> M{j + 1} : "
                f"{x[i][j]} containers"
            )

    print("Cout total :", cout_total)


# ==========================================
# 9. PROGRAMME PRINCIPAL
# ==========================================

if __name__ == "__main__":

    print("=" * 45)
    print("EXERCICE 2 - PROBLEME DE TRANSPORT")
    print("=" * 45)

    best, cout_tabou = recherche_tabou()

    afficher_solution(
        "RESULTAT DE LA RECHERCHE TABOUE",
        best,
        cout_tabou
    )

    optimum, cout_optimum = verification_exacte()

    afficher_solution(
        "VERIFICATION EXACTE",
        optimum,
        cout_optimum
    )

    print("\nComparaison finale :")

    print("Cout obtenu par recherche taboue :", cout_tabou)
    print("Cout optimal exact :", cout_optimum)

    if cout_tabou == cout_optimum:
        print("La recherche taboue a trouve l'optimum.")
    else:
        print("La recherche taboue n'a pas trouve l'optimum.")
