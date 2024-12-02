import asyncio
import pygame
import random
import math
import os
import sys

# Ensure the resources path works for web deployment
# You might need to adjust this path or use a different method for web resources
RESSOURCES = "ressources/"

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Pygame sprite classes (identical to previous implementation)
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

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pattern=None, speed=2, shot_rate=120):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        self.direction = 1
        self.pattern = pattern
        self.speed = speed
        self.shot_rate = shot_rate
        self.shot_counter = random.randint(0, shot_rate)
        
    def update(self):
        # Movement patterns
        if self.pattern == 'wave':
            # Wavy horizontal movement
            self.rect.x += self.speed * self.direction
            self.rect.y = self.original_y + math.sin(self.rect.x / 20) * 10
        elif self.pattern == 'zigzag':
            # Zigzag movement
            self.rect.x += self.speed * self.direction
            self.rect.y = self.original_y + math.sin(self.rect.x / 10) * 20
        else:
            # Default straight movement
            self.rect.x += self.speed * self.direction
        
        # Screen boundary and direction change
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            # Move down slightly when hitting boundary
            self.rect.y += 20
        
        # Shooting mechanism
        self.shot_counter += 1
        if self.shot_counter >= self.shot_rate:
            self.shoot()
            self.shot_counter = 0
    
    def shoot(self):
        # Randomly decide whether to shoot
        if random.random() < 0.5:
            missile = Missile(self.rect.centerx, self.rect.bottom, RED, 5)
            all_sprites.add(missile)
            alien_missiles.add(missile)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.lives = 15

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
        self.lives = 20
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
                missile = AngleMissile(self.rect.centerx, self.rect.bottom, RED, 5, angle)
                all_sprites.add(missile)
                alien_missiles.add(missile)
        
        elif self.attack_pattern == 1:
            # Homing missile attack
            if player:
                missile = HomingMissile(self.rect.centerx, self.rect.bottom, RED, player)
                all_sprites.add(missile)
                alien_missiles.add(missile)
        
        else:
            # Vertical laser attack
            for x in range(100, SCREEN_WIDTH-100, 100):
                laser = Laser(x, self.rect.bottom, BLUE)
                all_sprites.add(laser)
                alien_missiles.add(laser)

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

async def main():
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # Load images (modify to use web-friendly loading)
    global spaceship_img, alien_img1, alien_img2, alien_img3, boss_img
    try:
        spaceship_img = pygame.image.load(os.path.join(RESSOURCES, "vaisseau.png"))
        spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
        
        alien_img1 = pygame.image.load(os.path.join(RESSOURCES, "aliens.png"))
        alien_img1 = pygame.transform.scale(alien_img1, (40, 40))
        
        alien_img2 = pygame.image.load(os.path.join(RESSOURCES, "monstre.png"))
        alien_img2 = pygame.transform.scale(alien_img2, (40, 40))
        
        alien_img3 = pygame.image.load(os.path.join(RESSOURCES, "mechant.png"))
        alien_img3 = pygame.transform.scale(alien_img3, (40, 40))
        
        boss_img = pygame.image.load(os.path.join(RESSOURCES, "boss.png"))
        boss_img = pygame.transform.scale(boss_img, (200, 200))
    except Exception as e:
        print(f"Error loading images: {e}")
        return

    # Game initialization
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Game variables
    global score, level, game_over, boss, game_state, victory, player
    score = 0
    level = 1
    game_over = False
    boss = None
    game_state = "playing"
    victory = False

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
                
                # Quit option
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
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

            # Victory screen handling
            if game_state == "victory":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset game for replay
                        level = 1
                        score = 0
                        game_state = "playing"
                        game_over = False
                        victory = False
                        initialize_level(level)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

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

                    # Boss defeat check
                    if boss.lives <= 0:
                        level += 1
                        boss = None
                        game_state = "victory"
                        victory = True

            # Alien missiles and player collision detection
            player_collisions = pygame.sprite.spritecollide(player, alien_missiles, True)
            for collision in player_collisions:
                player.lives -= 1

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