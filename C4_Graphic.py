import pygame
import sys
from Codev3 import grille, modif, verif

pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)
ROUGE = (255, 0, 0)
TURQUOISE = (0, 128, 128)
GRIS_CLAIR = (211, 211, 211)

# Dimensions dynamiques de la fenêtre
LARGEUR, HAUTEUR = 700, 700
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Puissance 4")

FONT = pygame.font.Font(None, 36)

def saisir_pseudo(message, joueur_num):
    input_rect = pygame.Rect(LARGEUR // 4, HAUTEUR // 2 - 30, LARGEUR // 2, 60)
    nom = ""
    saisie_active = True
    curseur_visible = True
    curseur_timer = 0
    max_length = 15  # Longueur maximale du pseudo

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nom.strip():
                    return nom.strip()
                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                elif len(nom) < max_length and event.unicode.isalnum():
                    nom += event.unicode

        fenetre.fill(GRIS_CLAIR)

        # Affichage du titre
        titre = FONT.render(f"Joueur {joueur_num}", True, TURQUOISE)
        fenetre.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 4))

        # Affichage du message
        message_surface = FONT.render(message, True, NOIR)
        fenetre.blit(message_surface, (LARGEUR // 2 - message_surface.get_width() // 2, HAUTEUR // 2 - 80))

        # Dessin de la zone de saisie
        pygame.draw.rect(fenetre, NOIR, input_rect, 2)
        text_surface = FONT.render(nom, True, NOIR)
        fenetre.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # Affichage du curseur clignotant
        curseur_timer += 1
        if curseur_timer % 30 == 0:
            curseur_visible = not curseur_visible
        if saisie_active and curseur_visible:
            cursor_pos = FONT.size(nom)[0]
            pygame.draw.line(fenetre, NOIR, (input_rect.x + cursor_pos + 5, input_rect.y + 5),
                             (input_rect.x + cursor_pos + 5, input_rect.y + 55), 2)

        # Affichage du compteur de caractères
        counter = FONT.render(f"{len(nom)}/{max_length}", True, NOIR)
        fenetre.blit(counter, (input_rect.right - counter.get_width() - 10, input_rect.bottom + 10))

        # Bouton de validation
        valider_rect = pygame.Rect(LARGEUR // 2 - 75, HAUTEUR * 3 // 4, 150, 50)
        pygame.draw.rect(fenetre, TURQUOISE, valider_rect)
        valider_text = FONT.render("Valider", True, BLANC)
        fenetre.blit(valider_text, (valider_rect.centerx - valider_text.get_width() // 2, 
                                    valider_rect.centery - valider_text.get_height() // 2))

        # Vérification du clic sur le bouton Valider
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if valider_rect.collidepoint(mouse_pos) and click[0] == 1 and nom.strip():
            return nom.strip()

        pygame.display.flip()

def dessiner_grille(res):
    nb_lignes, nb_colonnes = len(res), len(res[0])

    # Hauteur de la banderole (15% de la hauteur totale)
    hauteur_banderole = int(HAUTEUR * 0.15)
    hauteur_grille = HAUTEUR - hauteur_banderole

    # Calcul des dimensions dynamiques
    largeur_cellule = LARGEUR / nb_colonnes
    hauteur_cellule = hauteur_grille / nb_lignes
    rayon_cercle = int(min(largeur_cellule, hauteur_cellule) / 2.5)

    # Dessiner les cercles pour chaque case
    fenetre.fill(GRIS_CLAIR)
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            # Calcul des coordonnées du centre des cercles
            x = int(colonne * largeur_cellule + largeur_cellule / 2)
            y = int(ligne * hauteur_cellule + hauteur_cellule / 2)

            # Déterminer la couleur en fonction de la valeur de la case
            couleur = NOIR if res[ligne][colonne] == 0 else (JAUNE if res[ligne][colonne] == 1 else ROUGE)

            # Dessiner un cercle pour représenter la case
            pygame.draw.circle(fenetre, couleur, (x, y), rayon_cercle)

    # Tracer les lignes de la grille
    for colonne in range(1, nb_colonnes):
        pygame.draw.line(fenetre, NOIR, (colonne * largeur_cellule, 0), (colonne * largeur_cellule, hauteur_grille), 2)
    for ligne in range(1, nb_lignes):
        pygame.draw.line(fenetre, NOIR, (0, ligne * hauteur_cellule), (LARGEUR, ligne * hauteur_cellule), 2)



def afficher_message(message, couleur_fond=TURQUOISE):
    hauteur_banderole = int(HAUTEUR * 0.15)  # Réserve 15% de l'écran pour la banderole
    pygame.draw.rect(fenetre, couleur_fond, [0, HAUTEUR - hauteur_banderole, LARGEUR, hauteur_banderole])

    texte = FONT.render(message, True, BLANC)
    text_rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR - hauteur_banderole // 2))
    fenetre.blit(texte, text_rect)


def main():
    # Afficher l'écran d'accueil
    ecran_accueil()

    # Saisie des pseudos
    pseudo_1 = saisir_pseudo("Nom joueur 1:", 1)
    pseudo_2 = saisir_pseudo("Nom joueur 2:", 2)

    # Initialisation de la grille
    res = grille()
    dessiner_grille(res)  # Dessin initial de la grille
    afficher_message(f"À {pseudo_1} de jouer !")  # Message initial
    pygame.display.update()  # Mise à jour de l'écran avant de commencer

    tour = 0
    partie_en_cours = True

    while partie_en_cours:
        for event in pygame.event.get():
            # Quitter le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion du redimensionnement de la fenêtre
            if event.type == pygame.VIDEORESIZE:
                global LARGEUR, HAUTEUR
                LARGEUR, HAUTEUR = event.w, event.h
                fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
                dessiner_grille(res)  # Redessiner la grille après redimensionnement
                afficher_message(f"À {pseudo_1 if tour % 2 == 0 else pseudo_2} de jouer !")
                pygame.display.update()

            # Gestion du clic pour jouer
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                colonne = int(event.pos[0] // (LARGEUR / 7))  # Calcul dynamique de la colonne
                if 0 <= colonne < 7:
                    # Vérifier si la colonne est pleine
                    if res[0][colonne] != 0:
                        afficher_message("Cette colonne est pleine, choisissez une autre !", couleur_fond=ROUGE)
                    else:
                        # Ajouter un jeton et mettre à jour le tour
                        tour += 1
                        res = modif(tour, colonne, res)
                        dessiner_grille(res)

                        # Vérification de victoire ou égalité
                        if verif(res, colonne) != 0:
                            gagnant = pseudo_1 if tour % 2 != 0 else pseudo_2
                            afficher_message(f"Victoire de {gagnant} !", couleur_fond=JAUNE if tour % 2 != 0 else ROUGE)
                            partie_en_cours = False
                        elif tour >= 42:
                            afficher_message("Égalité !", couleur_fond=TURQUOISE)
                            partie_en_cours = False
                        else:
                            joueur_actif = pseudo_1 if tour % 2 == 0 else pseudo_2
                            afficher_message(f"À {joueur_actif} de jouer !")

        pygame.display.update()

    # Pause avant de quitter le jeu
    pygame.time.wait(3000)  # Attente de 3 secondes avant de fermer la fenêtre
    pygame.quit()




def ecran_accueil():
    """Affiche l'écran d'accueil."""
    fenetre.fill(GRIS_CLAIR)
    message = FONT.render("Clic pour commencer le jeu", True, (0, 0, 255))
    fenetre.blit(message, [LARGEUR // 5, HAUTEUR - 100])
    pygame.display.update()
    
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                attente = False

if __name__ == "__main__":
    main()
