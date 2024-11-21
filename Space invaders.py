import pygame
import random
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
LARGEUR = 800
HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Space Invaders")

# Chemin vers le dossier ressources
RESSOURCES = r"C:\Users\tangu\OneDrive\Bureau\Autres projets\Jeu vidéo Python\ressources"

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Chargement des images
try: 
    vaisseau_img = pygame.image.load(os.path.join(RESSOURCES, "vaisseau.png"))
    vaisseau_img = pygame.transform.scale(vaisseau_img, (50, 50))
    
    alien_img1 = pygame.image.load(os.path.join(RESSOURCES, "aliens.png"))
    alien_img1 = pygame.transform.scale(alien_img1, (40, 40))
    
    alien_img2 = pygame.image.load(os.path.join(RESSOURCES, "monstre.png"))
    alien_img2 = pygame.transform.scale(alien_img2, (40, 40))
    
    alien_img3 = pygame.image.load(os.path.join(RESSOURCES, "mechant.png"))
    alien_img3 = pygame.transform.scale(alien_img3, (40, 40))
except pygame.error as e:
    print(f"Erreur de chargement des images : {e}")
    pygame.quit()
    exit()

# Classes du jeu
class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vaisseau_img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGEUR // 2
        self.rect.bottom = HAUTEUR - 10
        self.vitesse_x = 0
        self.vies = 30

    def update(self):
        self.rect.x += self.vitesse_x
        
        # Limites de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR

    def tirer(self):
        missile = Missile(self.rect.centerx, self.rect.top, BLANC, -10)
        tous_sprites.add(missile)
        missiles_joueur.add(missile)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, image, vitesse=2, taux_tir=120):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.compteur_tir = 0
        self.vitesse = vitesse
        self.taux_tir = taux_tir

    def update(self):
        self.rect.x += self.direction * self.vitesse
        
        # Changement de direction et descente
        if self.rect.right > LARGEUR or self.rect.left < 0:
            self.direction *= -1
            self.rect.y += 40

        # Tir aléatoire des aliens
        self.compteur_tir += 1
        if self.compteur_tir > self.taux_tir and random.random() < 0.1:  # Tir vraiment aléatoire
            self.tirer()
            self.compteur_tir = 0

    def tirer(self):
        missile = Missile(self.rect.centerx, self.rect.bottom, ROUGE, 5)
        tous_sprites.add(missile)
        missiles_aliens.add(missile)

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, couleur, vitesse_y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(couleur)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vitesse_y = vitesse_y

    def update(self):
        self.rect.y += self.vitesse_y
        
        # Supprimer le missile s'il sort de l'écran
        if self.rect.bottom < 0 or self.rect.top > HAUTEUR:
            self.kill()

def initialiser_niveau(numero_niveau):
    global joueur, tous_sprites, aliens, missiles_joueur, missiles_aliens, score
    
    # Réinitialiser les groupes de sprites
    tous_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    missiles_joueur = pygame.sprite.Group()
    missiles_aliens = pygame.sprite.Group()

    # Réinitialiser le joueur
    joueur = Vaisseau()
    tous_sprites.add(joueur)

    # Choisir l'image d'alien en fonction du niveau
    if numero_niveau == 1:
        alien_img = alien_img1
        lignes, colonnes = 5, 10
        vitesse_alien = 2
        taux_tir = 120
    elif numero_niveau == 2:
        alien_img = alien_img2
        lignes, colonnes = 6, 12
        vitesse_alien = 3
        taux_tir = 100
    else:
        alien_img = alien_img3
        lignes, colonnes = 7, 14
        vitesse_alien = 4
        taux_tir = 80

    # Créer les aliens
    for ligne in range(lignes):
        for colonne in range(colonnes):
            alien = Alien(colonne * 50 + 50, ligne * 50 + 50, alien_img, vitesse_alien, taux_tir)
            tous_sprites.add(alien)
            aliens.add(alien)
    
    # Réinitialiser le score (optionnel)
    if numero_niveau > 1:
        score += 50  # Bonus de score pour avoir passé un niveau

# Initialisation du jeu
police = pygame.font.Font(None, 36)
horloge = pygame.time.Clock()

# Sons (optionnel)
try:
    son_explosion = pygame.mixer.Sound(os.path.join(RESSOURCES, "explosion.wav"))
except:
    print("Pas de son d'explosion trouvé")
    son_explosion = None

# Variables du jeu
score = 0
niveau = 1
game_over = False

# Initialiser le premier niveau
initialiser_niveau(niveau)

# Boucle principale du jeu
en_cours = True
while en_cours:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        
        if game_over:
            # Option de rejouer
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Réinitialiser le jeu
                niveau = 1
                score = 0
                game_over = False
                initialiser_niveau(niveau)
        else:
            # Contrôles du joueur
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    joueur.vitesse_x = -5
                if event.key == pygame.K_RIGHT:
                    joueur.vitesse_x = 5
                if event.key == pygame.K_SPACE:
                    joueur.tirer()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    joueur.vitesse_x = 0

    if not game_over:
        # Mise à jour
        tous_sprites.update()

        # Détection de collisions missiles du joueur avec aliens
        collisions = pygame.sprite.groupcollide(missiles_joueur, aliens, True, True)
        for collision in collisions:
            score += 10
            if son_explosion:
                son_explosion.play()

        # Détection de collisions missiles aliens avec joueur
        collisions_joueur = pygame.sprite.spritecollide(joueur, missiles_aliens, True)
        for collision in collisions_joueur:
            joueur.vies -= 1
            if son_explosion:
                son_explosion.play()

        # Vérification de la progression des niveaux
        if len(aliens) == 0:
            niveau += 1
            if niveau <= 3:
                initialiser_niveau(niveau)
            else:
                game_over = True
                texte_victoire = police.render("Victoire Finale !", True, BLANC)

        # Vérification de la fin du jeu
        if joueur.vies <= 0:
            game_over = True
            texte_game_over = police.render("Game Over !", True, ROUGE)

    # Dessin
    fenetre.fill(NOIR)
    tous_sprites.draw(fenetre)

    # Affichage du score et des vies
    texte_score = police.render(f"Score : {score}", True, BLANC)
    texte_vies = police.render(f"Vies : {joueur.vies}", True, BLANC)
    texte_niveau = police.render(f"Niveau : {niveau}", True, BLANC)
    
    fenetre.blit(texte_score, (10, 10))
    fenetre.blit(texte_vies, (LARGEUR - 150, 10))
    fenetre.blit(texte_niveau, (LARGEUR // 2 - 50, 10))

    # Écran de fin de jeu
    if game_over:
        if niveau > 3:
            fenetre.blit(texte_victoire, (LARGEUR//2 - texte_victoire.get_width()//2, HAUTEUR//2))
        else:
            fenetre.blit(texte_game_over, (LARGEUR//2 - texte_game_over.get_width()//2, HAUTEUR//2))
        
        # Instructions pour rejouer
        texte_rejouer = police.render("Appuyez sur ESPACE pour rejouer", True, BLANC)
        fenetre.blit(texte_rejouer, (LARGEUR//2 - texte_rejouer.get_width()//2, HAUTEUR//2 + 50))

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limitation du framerate
    horloge.tick(60)

# Fermeture de Pygame
pygame.quit()