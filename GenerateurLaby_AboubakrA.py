from collections import deque

def existe_chemin(tableau):
    rows = len(tableau)
    cols = len(tableau[0])

    # Directions pour le déplacement (haut, bas, gauche, droite)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Vérifier si les coins sont accessibles
    if tableau[0][0] == "#" or tableau[-1][-1] == "#":
        return False

    # File pour BFS
    queue = deque([(1, 0)])  # Ajouter la position de départ
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    visited[1][0] = True  # Marquer la position de départ comme visitée

    while queue:
        x, y = queue.popleft()

        # Vérifier si nous sommes arrivés au coin en bas à droite
        if (x, y) == (rows - 1, cols - 1):
            return True

        # Explorer les voisins
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and tableau[nx][ny] == " ":
                queue.append((nx, ny))
                visited[nx][ny] = True

    # Si la file est vide et qu'on n'a pas trouvé le chemin, retourner False
    return False

# Exemple d'utilisation
if __name__ == "__main__":
    import random

    # Génération d'un tableau avec des bords et des coins vides
def generer_tableau_pondere(rows, cols, poids_sharp=3, poids_espace=7):
    # Création d'un tableau pondéré
    tableau = [
        [random.choices(["#", " "], weights=[poids_sharp, poids_espace])[0] for _ in range(cols)]
        for _ in range(rows)
    ]

    # Forcer les bords à être des `#`
    for i in range(rows):
        tableau[i][0] = "#"  # Première colonne
        tableau[i][-1] = "#"  # Dernière colonne

    for j in range(cols):
        tableau[0][j] = "#"  # Première ligne
        tableau[-1][j] = "#"  # Dernière ligne

    # Forcer les coins en haut à gauche et en bas à droite à être vides
    tableau[1][0] = " "
    tableau[-2][-1] = " "

    return tableau

def afficher_tableau(tableau):
    for row in tableau:
        print("".join(row))

if __name__ == "__main__":
    # Dimensions du tableau
    aleatoire = random.randint(4, 9)
    rows = cols = aleatoire

    # Génération du tableau pondéré
    tableau = generer_tableau_pondere(rows, cols, poids_sharp=3, poids_espace=7)

    # Affichage du tableau
    afficher_tableau(tableau)

    # Vérification de l'existence d'un chemin
    if existe_chemin(tableau):
        print("Il existe un chemin entre le coin en haut à gauche et le coin en bas à droite.")
    else:
        print("Aucun chemin n'existe entre le coin en haut à gauche et le coin en bas à droite.")
            
