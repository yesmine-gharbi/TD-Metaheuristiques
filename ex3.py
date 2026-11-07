import random
import math
import itertools



D = [
    [0, 14, 15, math.inf, math.inf, math.inf, math.inf, 17],
    [14, 0, 13, 14, 20, math.inf, math.inf, 21],
    [15, 13, 0, 11, 21, 17, 9, 9],
    [math.inf, 14, 11, 0, 11, 10, 8, 20],
    [math.inf, 20, 21, 11, 0, 15, 18, math.inf],
    [math.inf, math.inf, 17, 10, 15, 0, 9, math.inf],
    [math.inf, math.inf, 9, 8, 18, 9, 0, 13],
    [17, 21, 9, 20, math.inf, math.inf, 13, 0]
]


def calculer_cout(solution):

    total = 0

    for i in range(len(solution) - 1):

        distance = D[solution[i] - 1][solution[i + 1] - 1]

        if distance == math.inf:
            return math.inf

        total += distance

    # Retour a la premiere ville
    distance = D[solution[-1] - 1][solution[0] - 1]

    if distance == math.inf:
        return math.inf

    total += distance

    return total


def generer_voisins(solution):

    liste = []

    for i in range(1, 8):
        for j in range(i + 1, 8):

            voisin = solution.copy()

            voisin[i], voisin[j] = voisin[j], voisin[i]

            if calculer_cout(voisin) != math.inf:
                liste.append(voisin)

    return liste

def recherche_taboue():

    print("\n===== RECHERCHE TABOUE =====")

    solution = [1, 2, 3, 4, 5, 6, 7, 8]

    meilleure = solution.copy()

    taboue = []

    for iteration in range(30):

        liste = generer_voisins(solution)

        meilleur_voisin = None
        meilleur_cout = math.inf

        for voisin in liste:

            cout = calculer_cout(voisin)

            if voisin not in taboue or cout < calculer_cout(meilleure):

                if cout < meilleur_cout:
                    meilleur_cout = cout
                    meilleur_voisin = voisin

        if meilleur_voisin is None:
            break

        solution = meilleur_voisin.copy()

        taboue.append(solution.copy())

        if len(taboue) > 5:
            taboue.pop(0)

        if calculer_cout(solution) < calculer_cout(meilleure):
            meilleure = solution.copy()

        print("Iteration :", iteration + 1)
        print("Circuit :", solution)
        print("Cout :", calculer_cout(solution))

    print("\nMeilleur circuit :", meilleure)
    print("Cout final :", calculer_cout(meilleure))

def recuit_simule():

    print("\n===== RECUIT SIMULE =====")

    solution = [1, 2, 3, 4, 5, 6, 7, 8]

    meilleure = solution.copy()

    T = 10
    alpha = 0.8

    for iteration in range(5):

        liste = generer_voisins(solution)

        if len(liste) == 0:
            break

        voisin = random.choice(liste)

        delta = calculer_cout(voisin) - calculer_cout(solution)

        if delta <= 0:
            solution = voisin.copy()

        else:
            P = math.exp(-delta / T)

            nombre = random.random()

            if nombre < P:
                solution = voisin.copy()

        if calculer_cout(solution) < calculer_cout(meilleure):
            meilleure = solution.copy()

        print("Iteration :", iteration + 1)
        print("Temperature :", round(T, 3))
        print("Circuit :", solution)
        print("Cout :", calculer_cout(solution))

        T = T * alpha

    print("\nMeilleur circuit :", meilleure)
    print("Cout final :", calculer_cout(meilleure))


def croisement(parent1, parent2):

    debut = random.randint(1, 6)
    fin = random.randint(debut + 1, 7)

    enfant = [None] * 8

    enfant[0] = 1

    enfant[debut:fin + 1] = parent1[debut:fin + 1]

    reste = []

    for ville in parent2:
        if ville not in enfant:
            reste.append(ville)

    positions = []

    for i in range(1, 8):
        if enfant[i] is None:
            positions.append(i)

    for i in range(len(positions)):
        enfant[positions[i]] = reste[i]

    return enfant


def algorithme_genetique():

    print("\n===== ALGORITHME GENETIQUE =====")

    # Generer les circuits valides
    circuits = []

    for p in itertools.permutations(range(2, 9)):

        solution = [1] + list(p)

        if calculer_cout(solution) != math.inf:
            circuits.append(solution)

    # Population initiale
    population = random.sample(circuits, 10)

    generations = 20

    for generation in range(generations):

        population.sort(key=calculer_cout)

        # Garder les deux meilleurs
        nouvelle_population = population[:2]

        while len(nouvelle_population) < 10:

            # Selection
            parent1 = random.choice(population[:5])
            parent2 = random.choice(population[:5])

            # Croisement
            enfant = croisement(parent1, parent2)

            # Mutation
            if random.random() < 0.2:

                i, j = random.sample(range(1, 8), 2)

                enfant[i], enfant[j] = enfant[j], enfant[i]

            # Verifier la validite
            if calculer_cout(enfant) != math.inf:
                nouvelle_population.append(enfant)
            else:
                nouvelle_population.append(parent1.copy())

        population = nouvelle_population

        population.sort(key=calculer_cout)

        print("Generation :", generation + 1)
        print("Meilleur circuit :", population[0])
        print("Cout :", calculer_cout(population[0]))

    print("\nMeilleur circuit :", population[0])
    print("Cout final :", calculer_cout(population[0]))



print("COUT DE LA SOLUTION INITIALE :")

initiale = [1, 2, 3, 4, 5, 6, 7, 8]

print("Circuit :", initiale)
print("Cout :", calculer_cout(initiale))

recherche_taboue()

recuit_simule()

algorithme_genetique()
