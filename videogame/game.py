import os
import warnings

import pygame
import random



from .rgbcolors import black, white, red, green
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
        self.restart = False
        self.pause = False
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
            elif self.game_over:
                self.show_game_over_screen()

        pygame.quit()

    def show_start_screen(self):
        self.window.fill(black)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Space Invaders", True, white)
        start_text = font.render("Press Enter to Start", True, white)
        high_score_text = font.render("Press H to View High Scores", True, white)
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
        self.window.fill(black)
        font = pygame.font.Font(None, 36)
        title_text = font.render("High Scores", True, white)
        score1_text = font.render("1. Player1 - 1000", True, white)
        score2_text = font.render("2. Player2 - 800", True, white)
        score3_text = font.render("3. Player3 - 600", True, white)
        back_text = font.render("Press B to Go Back", True, white)
        self.window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
        self.window.blit(score1_text, (window_width // 2 - score1_text.get_width() // 2, 250))
        self.window.blit(score2_text, (window_width // 2 - score2_text.get_width() // 2, 300))
        self.window.blit(score3_text, (window_width // 2 - score3_text.get_width() // 2, 350))
        self.window.blit(back_text, (window_width // 2 - back_text.get_width() // 2, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.show_high_scores = False

    
    def game_loop(self):
        self.clock.tick(60)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_SPACE]:
            self.player.shoot()

        self.all_sprites.update()

        # Check for collisions between player bullets and enemies
        player_bullet_hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, enemies in player_bullet_hits.items():
            self.score += len(enemies)

        # Check for collisions between player and enemy bullets
        enemy_bullet_hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if enemy_bullet_hits:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True

        # Check for collisions between player bullets and obstacles
        player_bullet_obstacle_hits = pygame.sprite.groupcollide(self.bullets, self.obstacles, True, False)

        # Check for collisions between enemy bullets and obstacles
        enemy_bullet_obstacle_hits = pygame.sprite.groupcollide(self.enemy_bullets, self.obstacles, True, False)

        if not self.enemies:
            self.pause = True  
            self.show_pause_screen()  # Show the pause screen when there are no more enemies
            self.spawn_enemies()  # Respawn enemies after the pause

        self.window.fill(black)
        self.all_sprites.draw(self.window)
        self.draw_text(f"Score: {self.score}", 25, white, 50, 10)

        # Gain 1 life every 16 points
        if self.score >= 16 and self.score % 16 == 0 and self.score != self.prev_score:
            self.lives += 1
            self.prev_score = self.score
        elif self.score % 16 != 0:
            self.prev_score = 0

        self.draw_text(f"Lives: {self.lives}", 25, white, window_width - 50, 10)
        pygame.display.flip()

        if self.game_over:
            self.show_game_over_screen()

        # Pause and restart the game
        if self.game_over or self.start_screen or self.show_high_scores:
            return

        # Restart the game after the pause
        if self.pause:
            self.pause = False
            self.game_loop()


    def show_pause_screen(self):
        self.window.fill(black)
        font = pygame.font.Font(None, 36)
        pause_text = font.render("Congratulations, You Beat The Wave!", True, white)
        resume_text = font.render("Press any key to start the next Wave", True, white)
        self.window.blit(pause_text, (window_width // 2 - pause_text.get_width() // 2, 200))
        self.window.blit(resume_text, (window_width // 2 - resume_text.get_width() // 2, 300))
        pygame.display.flip()

        pygame.event.clear()  # Clear previous events

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                break



    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)

    def spawn_enemies(self):
        for row in range(4):
            for column in range(4):
                enemy = Enemy(self, column * (enemy_width + 10) + 50, row * (enemy_height + 10) + 50)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def spawn_obstacles(self):
        for column in range(4):
            obstacle = Obstacle(column * (obstacle_width + obstacle_spacing) + 200, window_height - 150)
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

    def show_game_over_screen(self):
        self.window.fill(black)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, white)
        restart_text = font.render("Press Enter to Restart", True, white)
        self.window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, 200))
        self.window.blit(restart_text, (window_width // 2 - restart_text.get_width() // 2, 300))
        pygame.display.flip()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.restart_game()

    def restart_game(self):
        self.game_over = False
        self.all_sprites.empty()
        self.bullets.empty()
        self.enemies.empty()
        self.enemy_bullets.empty()
        self.obstacles.empty()
        self.score = 0
        self.lives = 3
        self.spawn_enemies()
        self.spawn_obstacles()
        self.player = Player(self)
        self.all_sprites.add(self.player)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()

    def move_left(self):
        self.rect.x -= player_speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += player_speed
        if self.rect.x > window_width - player_width:
            self.rect.x = window_width - player_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, "up")
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.radius = enemy_width // 2
        self.image = pygame.Surface((enemy_width, enemy_height))
        #self.image.fill((red))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_direction = 1

        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)

    def update(self):
        self.rect.x += enemy_speed * self.x_direction
        if self.rect.x >= window_width - enemy_width or self.rect.x <= 0:
            self.y_move()
            self.x_direction *= -1

        if random.randint(0, 100) < 1:
            self.shoot()

    def y_move(self):
        self.rect.y += enemy_height

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, "down")
        self.game.all_sprites.add(bullet)
        self.game.enemy_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x - bullet_width // 2
        self.rect.y = y
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.rect.y -= bullet_speed
        elif self.direction == "down":
            self.rect.y += bullet_speed

        if self.rect.bottom < 0 or self.rect.top > window_height:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((obstacle_width, obstacle_height))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

