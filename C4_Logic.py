def pseudo():
    """Fonction pour demander les noms des deux joueurs."""
    Joueur1 = str(input("Joueur n°1, veuillez entrer un pseudonyme : "))
    Joueur2 = str(input("Joueur n°2, veuillez entrer un pseudonyme : "))
    print(f"Le pseudo du joueur n°1 est : {Joueur1}, le pseudo du joueur n°2 est : {Joueur2}")
    return Joueur1, Joueur2


def affichage(res: list):
    """Transforme la liste en format matrice pour l'affichage."""
    print("-" * 29)
    for ligne in res:
        s = "|"
        for case in ligne:
            if case == 0:
                s += "   |"
            elif case == 1:
                s += " J |"
            elif case == 2:
                s += " R |"
        print(s)
        print("-" * 29)


def grille() -> list:
    """Crée une grille vide (6x7) avec des zéros."""
    return [[0 for _ in range(7)] for _ in range(6)]


def modif(tour: int, colonne: int, res: list) -> list:
    """Ajoute un jeton dans la colonne sélectionnée si possible."""
    if colonne < 0 or colonne >= 7:
        print("Colonne invalide. Veuillez choisir une colonne entre 1 et 7.")
        return res

    # Trouver la première ligne vide dans la colonne
    for ligne in range(5, -1, -1):
        if res[ligne][colonne] == 0:
            res[ligne][colonne] = 1 if tour % 2 != 0 else 2
            return res

    print("Colonne pleine. Veuillez choisir une autre colonne.")
    return res


def verif(res: list, colonne: int) -> int:
    """Vérifie les conditions de victoire (verticale, horizontale, diagonale)."""
    nb_lignes, nb_colonnes = 6, 7
    joueur = 0

    # Rechercher la ligne où le jeton a été ajouté
    for ligne in range(nb_lignes):
        if res[ligne][colonne] != 0:
            joueur = res[ligne][colonne]
            break

    if joueur == 0:
        return 0  # Aucun jeton trouvé (impossible normalement)

    # Vérification verticale
    for i in range(max(0, ligne - 3), min(ligne + 1, nb_lignes - 3)):
        if all(res[i + k][colonne] == joueur for k in range(4)):
            return joueur

    # Vérification horizontale
    for start_col in range(max(0, colonne - 3), min(colonne + 1, nb_colonnes - 3)):
        if all(res[ligne][start_col + k] == joueur for k in range(4)):
            return joueur

    # Vérification diagonale (haut-gauche vers bas-droit)
    for d in range(-3, 1):
        if all(
            0 <= ligne + d + k < nb_lignes and 0 <= colonne + d + k < nb_colonnes and
            res[ligne + d + k][colonne + d + k] == joueur
            for k in range(4)
        ):
            return joueur

    # Vérification diagonale (haut-droit vers bas-gauche)
    for d in range(-3, 1):
        if all(
            0 <= ligne + d + k < nb_lignes and 0 <= colonne - d - k < nb_colonnes and
            res[ligne + d + k][colonne - d - k] == joueur
            for k in range(4)
        ):
            return joueur

    return 0  # Aucun gagnant


def jeu():
    """Lance le jeu avec une vérification de victoire ou égalité."""
    Joueur1, Joueur2 = pseudo()
    res = grille()
    affichage(res)
    tour = 0
    victoire = 0

    while tour < 42 and victoire == 0:
        try:
            colonne = int(input(f"Tour {tour + 1} : choisissez une colonne (1-7) : ")) - 1
            tour += 1
            res = modif(tour, colonne, res)
            affichage(res)
            victoire = verif(res, colonne)
        except ValueError:
            print("Entrée invalide, veuillez entrer un chiffre entre 1 et 7.")

    if victoire != 0:
        gagnant = Joueur1 if victoire == 1 else Joueur2
        print(f"Félicitations, {gagnant} a gagné !")
    else:
        print("Match nul ! Aucune victoire.")


if __name__ == "__main__":
    jeu()