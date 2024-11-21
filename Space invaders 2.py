import pygame
import random
import os
import math

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Path to resources folder
RESOURCES = r"C:\Users\tangu\OneDrive\Bureau\Autres projets\Jeu vidéo Python\ressources"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load images
try:
    spaceship_img = pygame.image.load(os.path.join(RESOURCES, "vaisseau.png"))
    spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
    
    alien_img1 = pygame.image.load(os.path.join(RESOURCES, "aliens.png"))
    alien_img1 = pygame.transform.scale(alien_img1, (40, 40))
    
    alien_img2 = pygame.image.load(os.path.join(RESOURCES, "monstre.png"))
    alien_img2 = pygame.transform.scale(alien_img2, (40, 40))
    
    alien_img3 = pygame.image.load(os.path.join(RESSOURCES, "mechant.png"))
    alien_img3 = pygame.transform.scale(alien_img3, (40, 40))
    
    boss_img = pygame.image.load(os.path.join(RESOURCES, "boss.png"))
    boss_img = pygame.transform.scale(boss_img, (200, 200))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Missile Class
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed_y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        
        # Remove missile if it goes out of screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Angle Missile Class
class AngleMissile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, angle):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed
        self.angle = math.radians(angle)
        self.speed_x = self.speed * math.sin(self.angle)
        self.speed_y = self.speed * math.cos(self.angle)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Remove missile if it goes out of screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()

# Homing Missile Class
class HomingMissile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, target):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 3
        self.target = target

    def update(self):
        # Guide missile towards the player
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
        
        # Remove missile if it goes out of screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Laser Class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, SCREEN_HEIGHT))
        self.image.fill(color)
        self.image.set_alpha(100)  # Make laser semi-transparent
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.duration = 60  # Laser duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()

# Spaceship Class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.lives = 3

    def update(self):
        self.rect.x += self.speed_x
        
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        missile = Missile(self.rect.centerx, self.rect.top, WHITE, -10)
        all_sprites.add(missile)
        player_missiles.add(missile)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 50
        self.lives = 100
        self.attack_counter = 0
        self.attack_pattern = 0

    def update(self):
        self.attack_counter += 1
        
        # Change attack pattern every 180 frames
        if self.attack_counter >= 180:
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.attack()
            self.attack_counter = 0

    def attack(self):
        if self.attack_pattern == 0:
            # Fan missile attack
            angles = [-45, -30, -15, 0, 15, 30, 45]
            for angle in angles:
                missile = anglemissile(self.rect.centerx, self.rect.bottom, RED, 5, angle)
                all_sprites.add(missile)
                alien_missiles.add(missile)
        
        elif self.attack_pattern == 1:
            # Homing missile attack
            if player:
                missile = Homingmissile(self.rect.centerx, self.rect.bottom, RED, player)
                all_sprites.add(missile)
                alien_missiles.add(missile)
        
        else:
            # Vertical laser attack
            for x in range(100, SCREEN_WIDTH-100, 100):
                laser = Laser(x, self.rect.bottom, BLUE)
                all_sprites.add(laser)
                alien_missiles.add(laser)

# Add remaining classes (missile, Anglemissile, Homingmissile, Laser) 
# following the same translation pattern as above

def initialize_level(level_number):
    global player, all_sprites, aliens, player_missiles, alien_missiles, boss, score
    
    # Reset sprite groups
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    player_missiles = pygame.sprite.Group()
    alien_missiles = pygame.sprite.Group()

    # Reset player
    player = Spaceship()
    all_sprites.add(player)

    # Choose alien image based on level
    if level_number == 1:
        alien_img = alien_img1
        rows, cols = 5, 10
        alien_speed = 2
        shot_rate = 120
        pattern = None
    elif level_number == 2:
        alien_img = alien_img2
        rows, cols = 5, 10
        alien_speed = 3
        shot_rate = 100
        pattern = 'wave'
    elif level_number == 3:
        alien_img = alien_img3
        rows, cols = 5, 10
        alien_speed = 4
        shot_rate = 80
        pattern = 'zigzag'
    elif level_number == 4:
        # Boss level
        boss = Boss()
        all_sprites.add(boss)
        return

    # Create aliens
    for row in range(rows):
        for col in range(cols):
            # Calculate position with some randomization
            x = col * 60 + 50 + random.randint(-20, 20)
            y = row * 50 + 50 + random.randint(-20, 20)
            alien = Alien(x, y, alien_img, pattern, alien_speed, shot_rate)
            all_sprites.add(alien)
            aliens.add(alien)
    
    # Score bonus for passing a level
    if level_number > 1:
        score += 50

# Game initialization
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Sounds (optional)
try:
    explosion_sound = pygame.mixer.Sound(os.path.join(RESOURCES, "explosion.mp3"))
except:
    print("No explosion sound found")
    explosion_sound = None

# Game variables
score = 0
level = 1
game_over = False
boss = None

# Initialize first level
initialize_level(level)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_over:
            # Replay option
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset game
                level = 1
                score = 0
                game_over = False
                initialize_level(level)
        else:
            # Player controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed_x = -5
                if event.key == pygame.K_RIGHT:
                    player.speed_x = 5
                if event.key == pygame.K_SPACE:
                    player.shoot()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.speed_x = 0

    # Clear screen
    screen.fill(BLACK)

    if not game_over:
        # Update
        all_sprites.update()

        # Level management
        if level <= 3:
            # Player missile and alien collision detection
            collisions = pygame.sprite.groupcollide(player_missiles, aliens, True, True)
            for collision in collisions:
                score += 10
                if explosion_sound:
                    explosion_sound.play()

            # Level progression check
            if len(aliens) == 0:
                level += 1
                initialize_level(level)

        elif level == 4:
            # Boss level
            if boss:
                # Boss collision detection
                boss_collisions = pygame.sprite.groupcollide(player_missiles, [boss], True, False)
                for collision in boss_collisions:
                    boss.lives -= 1
                    score += 5
                    if explosion_sound:
                        explosion_sound.play()

                # Boss defeat check
                if boss.lives <= 0:
                    level += 1
                    boss = None

        # Alien missiles and player collision detection
        player_collisions = pygame.sprite.spritecollide(player, alien_missiles, True)
        for collision in player_collisions:
            player.lives -= 1
            if explosion_sound:
                explosion_sound.play()

        # Game over check
        if player.lives <= 0:
            game_over = True
        
        # Draw all sprites
        all_sprites.draw(screen)

        # Display score and player lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    else:
        # Game Over screen
        game_over_text = font.render("Game Over", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        replay_text = font.render("Press [Space] to Replay", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 1.5))

    # Update display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()