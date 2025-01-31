from config import WALL, EMPTY, Coord
from random import shuffle

patterns = (
        (0,-1), (0,1), (-1,0), (1,0)
        ) # haut, bas, gauche, droite


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def is_valid_case(self, case: Coord) -> bool:
        return 0 <= case[1] <= self.height-1 and 0 <= case[0] <= self.width-1 # erreur est ici, essaie de la trouver, ducoup ?

    def generate(self) -> list[list[int]]:

        # on crée une grille vide
        grid = [[WALL for _ in range(self.width)] for _ in range(self.height)] # non ici on a bien
        start, finish = (0, 0), (self.width - 1, self.height - 1)


        # implémentation de la fonction avancer

        def move(current_case, last_case=None): # pourquoi par défaut None ? parce que quand on part de la case départ il n'y a pas de case avant
            # on doit vérifier si on est arrivé à la case finale
            if current_case == finish: # on ne veut pas continuer de chemin si on est à la case finale pour pas créer de chemins suplémentaires
                return

            # cases autour (excepté la case "last_case" d'où on vient)
            ok = True

            cases = []
            for pattern in patterns:
                case = (pattern[0] + current_case[0], pattern[1] + current_case[1]) 
                if self.is_valid_case(case):
                    if last_case and case != last_case:
                        cases.append(case)
                    elif not last_case:
                        cases.append(case)

            for c in cases:
                if self.is_valid_case(c) and grid[c[1]][c[0]] == EMPTY:
                    ok = False
                    break
            if not ok: # on fait simplement ici le return avant mais on aurait pu le faire après
                return

            # on colorie la case sur laquelle on est
            grid[current_case[1]][current_case[0]] = EMPTY

            # on bouge (il faudrait le faire de manière aléatoire) ~> changer l'ordre des éléments de la liste (tu peux faire une petite recherche google), il y a une fonction spéciale pour ça

            shuffle(cases)            
            for case in cases:
                if self.is_valid_case(case):
                    move(case, current_case)
                    

        move(start)

        # on vérifie que l'entrée et la sortie sont vides
        grid[start[1]][start[0]] = EMPTY
        grid[finish[1]][finish[0]] = EMPTY

        return grid, start, finish
