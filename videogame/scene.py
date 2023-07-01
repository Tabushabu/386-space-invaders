# Kyler Farnsworth
# KFarnsworth1@csu.fullerton.edu
# @Tabushabu

import pygame


class Scene(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 600))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class StartScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.title = self.font.render("Space Invaders", True, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(400, 250))

    def draw(self, window):
        window.blit(self.title, self.title_rect)


class GameOverScene(Scene):
    def __init__(self, score, is_high_score):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.game_over_text = self.font.render("Game Over", True, (0, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(400, 250))
        self.score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))
        self.score_rect = self.score_text.get_rect(center=(400, 300))

        if is_high_score:
            self.high_score_text = self.font.render("New High Score!", True, (0, 0, 0))
            self.high_score_rect = self.high_score_text.get_rect(center=(400, 350))

    def draw(self, window):
        window.blit(self.game_over_text, self.game_over_rect)
        window.blit(self.score_text, self.score_rect)

        if hasattr(self, 'high_score_text'):
            window.blit(self.high_score_text, self.high_score_rect)


def run_game():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders")

    scenes = {
        'start': StartScene(),
        'game': GameScene(),
        'game_over': GameOverScene(),
    }

    current_scene = scenes['start']

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_scene.draw(window)

        pygame.display.flip()

    pygame.quit()
