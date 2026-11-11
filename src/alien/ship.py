from pathlib import Path

import pygame

import alien.alien_invasion as Ai

class Ship:
    def __init__(self, ai_game: Ai) -> None:
        self.screen = ai_game.screen
        self.config = ai_game.config
        self.screen_rect = ai_game.screen.get_rect()

        BASE_DIR = Path(__file__).resolve().parent / self.config.imagen_ship

        self.image = pygame.image.load(BASE_DIR).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

    def update(self):
        ship_speed = self.config.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= ship_speed

        self.rect.x = self.x
    def blitme(self):
        self.screen.blit(self.image, self.rect)
