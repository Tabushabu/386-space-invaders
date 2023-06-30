import os
import warnings

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
        self.start_screen = True
        self.show_high_scores = False
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

        self.window = pygame.display.set_mode((window_width, window_height))
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

        self.player = Player(self)
        self.all_sprites.add(self.player)

        while self.running:
            if self.start_screen:
                self.show_start_screen()
            elif self.show_high_scores:
                self.show_high_score_screen()
            elif not self.game_over:
                self.game_loop()

        pygame.quit()

    def show_start_screen(self):
        self.window.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Space Invaders", True, WHITE)
        start_text = font.render("Press Enter to Start", True, WHITE)
        high_score_text = font.render("Press H to View High Scores", True, WHITE)
        self.window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
        self.window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, 300))
        self.window.blit(high_score_text, (window_width // 2 - high_score_text.get_width() // 2, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_screen = False
                elif event.key == pygame.K_h:
                    self.show_high_scores = True

    def show_high_score_screen(self):
        self.window.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title_text = font.render("High Scores", True, WHITE)
        score1_text = font.render("1. Player1 - 1000", True, WHITE)
        score2_text = font.render("2. Player2 - 800", True, WHITE)
        score3_text = font.render("3. Player3 - 600", True, WHITE)
        back_text = font.render("Press B to Go Back", True, WHITE)
        self.window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
        self.window.blit(score1_text, (window_width // 2 - score1_text.get_width() // 2, 300))
        self.window.blit(score2_text, (window_width // 2 - score2_text.get_width() // 2, 350))
        self.window.blit(score3_text, (window_width // 2 - score3_text.get_width() // 2, 400))
        self.window.blit(back_text, (window_width // 2 - back_text.get_width() // 2, 500))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.show_high_scores = False

    def game_loop(self):
        self.handle_events()

        if not self.game_over:
            self.update()

        self.draw()

        self.clock.tick(60)

    def spawn_enemies(self):
        for row in range(4):
            for col in range(4):
                x = col * (enemy_width + 10)
                y = row * (enemy_height + 10)
                enemy = Enemy(x, y + 50, self.enemy_bullets, self)
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
        pygame.sprite.groupcollide(self.obstacles, self.enemy_bullets, False, True)

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

        if self.score >= 16 and self.score % 16 == 0 and self.score != self.prev_score:
            self.lives += 1
            self.prev_score = self.score
        elif self.score % 16 != 0:
            self.prev_score = 0

    def draw(self):
        self.window.fill(BLACK)
        self.all_sprites.draw(self.window)
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        lives_text = font.render("Lives: " + str(self.lives), True, WHITE)
        self.window.blit(score_text, (window_width - score_text.get_width() - 10, 10))
        self.window.blit(lives_text, (10, 10))
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.x > window_width - player_width:
            self.rect.x = window_width - player_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

    def reset_position(self):
        self.rect.x = player_x
        self.rect.y = player_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = bullet_speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((enemy_width, enemy_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = enemy_speed
        self.bullets = bullets
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000

    def update(self):
        self.rect.x += self.speed
        self.handle_edge_collision()
        self.try_shoot()

    def handle_edge_collision(self):
        if self.rect.right > window_width or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += enemy_height

    def try_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and len(self.bullets) < 3:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            self.game.all_sprites.add(bullet)
            self.bullets.add(bullet)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((obstacle_width, obstacle_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
