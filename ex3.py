
import random
import math
from itertools import permutations
from collections import deque

# ==================================================
# 1. DONNEES DU PROBLEME
# ==================================================

random.seed(1)

INF = float("inf")

# Couts des liaisons indiquees dans le sujet
aretes = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17,
    (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13
}

VILLES = list(range(1, 9))
SOLUTION_INITIALE = [1, 2, 3, 4, 5, 6, 7, 8]


# ==================================================
# 2. FONCTIONS DE BASE
# ==================================================

def distance(a, b):
    """Retourne le cout d'une liaison, ou INF si elle est absente."""
    return aretes.get(
        (a, b),
        aretes.get((b, a), INF)
    )


def cout_tour(tour):
    """Calcule le cout du circuit, retour a la ville de depart inclus."""
    total = 0

    for i in range(len(tour)):
        a = tour[i]
        b = tour[(i + 1) % len(tour)]

        c = distance(a, b)

        if c == INF:
            return INF

        total += c

    return total


def tour_valide(tour):
    """Verifie que toutes les liaisons du circuit existent."""
    return cout_tour(tour) != INF


def afficher_tour(tour):
    """Affiche le circuit en ajoutant le retour a la ville 1."""
    return " -> ".join(map(str, tour + [tour[0]]))


def echanger(tour, i, j):
    """Construit un voisin en echangeant deux villes."""
    resultat = tour[:]
    resultat[i], resultat[j] = resultat[j], resultat[i]
    return resultat


# ==================================================
# 3. RECHERCHE TABOUE
# ==================================================

def recherche_taboue(nb_iter=100, taille_tabou=7):
    courant = SOLUTION_INITIALE[:]
    meilleur = courant[:]
    meilleur_cout = cout_tour(meilleur)

    liste_taboue = deque(maxlen=taille_tabou)

    print("\n" + "=" * 55)
    print("RECHERCHE TABOUE")
    print("=" * 55)

    print("Circuit initial :", afficher_tour(courant))
    print("Cout initial :", cout_tour(courant))

    for iteration in range(1, nb_iter + 1):
        meilleur_voisin = None
        cout_voisin = INF
        mouvement_choisi = None

        # La ville 1 reste fixe en premiere position
        for i in range(1, len(courant) - 1):
            for j in range(i + 1, len(courant)):
                voisin = echanger(courant, i, j)

                # Ignorer les circuits utilisant une liaison absente
                if not tour_valide(voisin):
                    continue

                mouvement = tuple(sorted((courant[i], courant[j])))
                est_tabou = mouvement in liste_taboue
                cout = cout_tour(voisin)

                # Critere d'aspiration :
                # autoriser un mouvement tabou s'il ameliore le meilleur
                if est_tabou and cout >= meilleur_cout:
                    continue

                if cout < cout_voisin:
                    meilleur_voisin = voisin
                    cout_voisin = cout
                    mouvement_choisi = mouvement

        if meilleur_voisin is None:
            print("Aucun voisin admissible. Fin de la recherche.")
            break

        courant = meilleur_voisin
        liste_taboue.append(mouvement_choisi)

        if cout_voisin < meilleur_cout:
            meilleur = courant[:]
            meilleur_cout = cout_voisin

        print(
            f"Iteration {iteration:3d} | "
            f"Cout courant = {cout_voisin:3.0f} | "
            f"Meilleur cout = {meilleur_cout:3.0f}"
        )

    print("\nMeilleur circuit tabou :", afficher_tour(meilleur))
    print("Meilleur cout tabou :", meilleur_cout)

    return meilleur, meilleur_cout


# ==================================================
# 4. RECUIT SIMULE
# ==================================================

def recuit_simule(
    nb_iter=5,
    temperature_initiale=20.0,
    alpha=0.8
):
    courant = SOLUTION_INITIALE[:]
    meilleur = courant[:]

    cout_courant = cout_tour(courant)
    meilleur_cout = cout_courant
    temperature = temperature_initiale

    print("\n" + "=" * 55)
    print("RECUIT SIMULE")
    print("=" * 55)

    print("Circuit initial :", afficher_tour(courant))
    print("Cout initial :", cout_courant)
    print("Temperature initiale :", temperature_initiale)
    print("Coefficient de refroidissement :", alpha)

    for iteration in range(1, nb_iter + 1):

        # Choisir deux positions differentes, sans deplacer la ville 1
        i, j = random.sample(range(1, len(courant)), 2)

        candidat = echanger(courant, i, j)
        cout_candidat = cout_tour(candidat)

        # Une liaison absente rend le candidat inadmissible
        if cout_candidat == INF:
            print(
                f"Iteration {iteration} : "
                "candidat invalide, mouvement refuse."
            )
            temperature *= alpha
            continue

        delta = cout_candidat - cout_courant

        if delta <= 0:
            probabilite = 1.0
        else:
            probabilite = math.exp(-delta / temperature)

        tirage = random.random()
        accepte = tirage < probabilite

        if accepte:
            courant = candidat
            cout_courant = cout_candidat

        if cout_courant < meilleur_cout:
            meilleur = courant[:]
            meilleur_cout = cout_courant

        print(
            f"Iteration {iteration:2d} | "
            f"T = {temperature:7.3f} | "
            f"delta = {delta:4.0f} | "
            f"P = {probabilite:.3f} | "
            f"tirage = {tirage:.3f} | "
            f"{'accepte' if accepte else 'refuse'} | "
            f"cout courant = {cout_courant:.0f} | "
            f"meilleur = {meilleur_cout:.0f}"
        )

        # Refroidissement
        temperature *= alpha

    print("\nMeilleur circuit recuit :", afficher_tour(meilleur))
    print("Meilleur cout recuit :", meilleur_cout)

    return meilleur, meilleur_cout


# ==================================================
# 5. ALGORITHME GENETIQUE
# ==================================================

def generer_tour_valide():
    """Genere un circuit valide en gardant la ville 1 au debut."""
    autres_villes = VILLES[1:]

    for _ in range(10000):
        random.shuffle(autres_villes)
        candidat = [1] + autres_villes[:]

        if tour_valide(candidat):
            return candidat

    raise RuntimeError("Impossible de generer un circuit valide.")


def croisement(parent1, parent2):
    """Croisement d'ordre (Order Crossover, OX)."""
    taille = len(parent1)

    i, j = sorted(random.sample(range(1, taille), 2))

    enfant = [None] * taille
    enfant[0] = 1

    # Copier un segment du premier parent
    enfant[i:j + 1] = parent1[i:j + 1]

    villes_restantes = [
        ville for ville in parent2[1:]
        if ville not in enfant
    ]

    positions = [
        k for k in range(1, taille)
        if enfant[k] is None
    ]

    for position, ville in zip(positions, villes_restantes):
        enfant[position] = ville

    return enfant


def mutation(tour, probabilite=0.2):
    """Echange deux villes avec une certaine probabilite."""
    resultat = tour[:]

    if random.random() < probabilite:
        i, j = random.sample(range(1, len(resultat)), 2)
        resultat[i], resultat[j] = resultat[j], resultat[i]

    return resultat


def algorithme_genetique(
    taille_population=40,
    nb_generations=200,
    taux_mutation=0.2
):
    print("\n" + "=" * 55)
    print("ALGORITHME GENETIQUE")
    print("=" * 55)

    # Initialisation de la population
    population = [SOLUTION_INITIALE[:]]

    while len(population) < taille_population:
        candidat = generer_tour_valide()

        if candidat not in population:
            population.append(candidat)

    meilleur = None
    meilleur_cout = INF

    for generation in range(1, nb_generations + 1):

        population.sort(key=cout_tour)

        if cout_tour(population[0]) < meilleur_cout:
            meilleur = population[0][:]
            meilleur_cout = cout_tour(meilleur)

        # Conserver les deux meilleurs individus
        nouvelle_population = [
            population[0][:],
            population[1][:]
        ]

        # Selection par tournoi, entre trois individus
        while len(nouvelle_population) < taille_population:

            candidats1 = random.sample(
                population,
                min(3, len(population))
            )
            parent1 = min(candidats1, key=cout_tour)

            candidats2 = random.sample(
                population,
                min(3, len(population))
            )
            parent2 = min(candidats2, key=cout_tour)

            enfant = croisement(parent1, parent2)
            enfant = mutation(enfant, taux_mutation)

            # Ne conserver que les circuits valides
            if tour_valide(enfant):
                nouvelle_population.append(enfant)
            else:
                # Si le descendant est invalide, utiliser
                # un circuit valide aleatoire
                nouvelle_population.append(generer_tour_valide())

        population = nouvelle_population

        if generation % 20 == 0 or generation == 1:
            print(
                f"Generation {generation:3d} | "
                f"Meilleur cout = {meilleur_cout:.0f}"
            )

    # Derniere verification de la population
    population.sort(key=cout_tour)

    if cout_tour(population[0]) < meilleur_cout:
        meilleur = population[0][:]
        meilleur_cout = cout_tour(meilleur)

    print("\nMeilleur circuit genetique :", afficher_tour(meilleur))
    print("Meilleur cout genetique :", meilleur_cout)

    return meilleur, meilleur_cout


# ==================================================
# 6. VERIFICATION EXACTE
# ==================================================

def optimum_exact():
    """Teste tous les circuits possibles commencant par la ville 1."""
    meilleur = None
    meilleur_cout = INF

    for permutation in permutations(range(2, 9)):
        tour = [1] + list(permutation)
        cout = cout_tour(tour)

        if cout < meilleur_cout:
            meilleur = tour[:]
            meilleur_cout = cout

    return meilleur, meilleur_cout


# ==================================================
# 7. PROGRAMME PRINCIPAL
# ==================================================

if __name__ == "__main__":

    print("PROBLEME DU VOYAGEUR DE COMMERCE")
    print("Nombre de villes :", len(VILLES))
    print("Circuit initial :", afficher_tour(SOLUTION_INITIALE))
    print("Cout initial :", cout_tour(SOLUTION_INITIALE))

    # Question 1 : recherche taboue
    meilleur_tabou, cout_tabou = recherche_taboue(
        nb_iter=100,
        taille_tabou=7
    )

    # Question 2 : recuit simule, 5 iterations
    meilleur_recuit, cout_recuit = recuit_simule(
        nb_iter=5,
        temperature_initiale=20.0,
        alpha=0.8
    )

    # Question 3 : algorithme genetique
    meilleur_genetique, cout_genetique = algorithme_genetique(
        taille_population=40,
        nb_generations=200,
        taux_mutation=0.2
    )

    # Verification exacte supplementaire
    meilleur_exact, cout_exact = optimum_exact()

    print("\n" + "=" * 55)
    print("COMPARAISON FINALE")
    print("=" * 55)

    print(
        f"Recherche taboue : {afficher_tour(meilleur_tabou)} "
        f"| cout = {cout_tabou}"
    )

    print(
        f"Recuit simule    : {afficher_tour(meilleur_recuit)} "
        f"| cout = {cout_recuit}"
    )

    print(
        f"Algorithme genetique : "
        f"{afficher_tour(meilleur_genetique)} "
        f"| cout = {cout_genetique}"
    )

    print(
        f"Optimum exact    : {afficher_tour(meilleur_exact)} "
        f"| cout = {cout_exact}"
    )
