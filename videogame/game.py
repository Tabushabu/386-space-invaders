import pygame
import random
from .rgbcolors import BLACK, WHITE
from .scene import Scene
from .setup import (
    window_width, window_height, player_x, player_y, player_width, player_height, player_speed,
    enemy_width, enemy_height, enemy_speed, bullet_width, bullet_height, bullet_speed,
    obstacle_width, obstacle_height, obstacle_spacing
)


class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.all_sprites = None
        self.bullets = None
        self.enemies = None
        self.enemy_bullets = None
        self.obstacles = None
        self.score = 0
        self.lives = 3
        self.player = None
        self.clock = pygame.time.Clock()

    def run_game(self):
        pygame.init()

        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Space Invaders")

        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.score = 0
        self.lives = 3
        self.spawn_enemies()
        self.spawn_obstacles()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.game_loop(window)

        pygame.quit()

    def spawn_enemies(self):
        for row in range(4):
            for col in range(4):
                x = col * (enemy_width + 10)
                y = row * (enemy_height + 10)
                enemy = Enemy(x, y + 50, self.enemy_bullets)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def spawn_obstacles(self):
        for i in range(2):
            x = (window_width - (obstacle_width + obstacle_spacing) * 2) // 2 + (obstacle_width + obstacle_spacing) * i
            y = window_height - obstacle_height - 100
            obstacle = Obstacle(x, y)
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_SPACE]:
            self.player.shoot()

    def update(self):
        self.all_sprites.update()

        # Check for collision between bullets and enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for enemy in hits:
            self.score += 1

        # Check for collision between player and enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.player.reset_position()

        # Check for collision between bullets and obstacles
        pygame.sprite.groupcollide(self.obstacles, self.bullets, False, True)
        pygame.sprite.groupcollide(self.obstacles, self.enemy_bullets,False, True)

        # Check for collision between enemy bullets and player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.player.reset_position()

        if self.game_over:
            self.running = False  # Set running to False if game over


    def draw(self, window):
        window.fill(BLACK)
        self.all_sprites.draw(window)

        # Draw score counter
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        window.blit(score_text, (10, 10))

        # Draw life counter
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        window.blit(lives_text, (window_width - lives_text.get_width() - 10, 10))

        pygame.display.flip()

    def game_loop(self, window):
        while self.running:
            self.handle_events()

            if not self.game_over:
                self.update()

            self.draw(window)
            self.clock.tick(60)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= player_speed

    def move_right(self):
        if self.rect.right < window_width:
            self.rect.x += player_speed

    def shoot(self):
        bullet = Bullet(self.rect.x + player_width // 2 - bullet_width // 2, self.rect.y, -bullet_speed)
        game.bullets.add(bullet)
        game.all_sprites.add(bullet)

    def reset_position(self):
        self.rect.x = player_x
        self.rect.y = player_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_bullets):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((enemy_width, enemy_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.enemy_bullets = enemy_bullets
        self.shoot_delay = random.randint(1000, 3000)
        self.last_shot_time = pygame.time.get_ticks()
        self.direction = 1  # 1 represents moving to the right, -1 represents moving to the left

    def update(self):
        self.rect.x += enemy_speed * self.direction

        # Check if the group of enemies reaches the edge of the window
        if self.rect.right >= window_width or self.rect.left <= 0:
            self.direction *= -1  # Reverse the direction
            self.rect.y += enemy_height  # Move down one unit

        self.shoot()



    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            bullet = Bullet(self.rect.x + enemy_width // 2 - bullet_width // 2, self.rect.y + enemy_height, bullet_speed)
            self.enemy_bullets.add(bullet)
            game.all_sprites.add(bullet)
            self.last_shot_time = current_time


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((obstacle_width, obstacle_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


game = Game()
game.run_game()
