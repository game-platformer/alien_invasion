from pathlib import Path

import pygame
from pygame.sprite import Sprite

from alien import alien_invasion as ai


class Alien(Sprite):
    def __init__(self, ai_game: ai):
        super().__init__()
        self.screen = ai_game.screen
        self.config = ai_game.config

        ruta = Path(__file__).parent / 'assets/alien.bmp'
        self.image = pygame.image.load(ruta)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = self.rect.x

    def check_edges(self) -> bool:
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.config.alien_speed * self.config.fleet_direction
        self.rect.x = self.x
