import random  # On importe les bibliothèques

aleatoire = random.randint(4, 9)
print(aleatoire)

rows = aleatoire
cols = aleatoire

# Générer le tableau avec des '#' ou des espaces
tableau = [[random.choice(["#", " "]) for _ in range(cols)] for _ in range(rows)]

# Forcer les bords à être des '#'
for i in range(rows):
    tableau[i][0] = "#"  # Première colonne
    tableau[i][-1] = "#"  # Dernière colonne

for j in range(cols):
    tableau[0][j] = "#"  # Première ligne
    tableau[-1][j] = "#"  # Dernière ligne

# Forcer les coins en haut à gauche et en bas à droite à être vides
tableau[1][0] = " "  # Coin en haut à gauche
tableau[-2][-1] = " "  # Coin en bas à droite

# Afficher le tableau
for row in tableau:
    print("".join(row))