import sys

import pygame

from config.configuration import Configuration
from .bullet import Bullet

from .ship import Ship

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.config = Configuration()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.config.screen_height = self.screen.get_height()
        self.config.screen_width = self.screen.get_width()

        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

    def run_game(self):
        running = True
        while running:
            self._check_events()

            self.ship.update()
            self.bullets.update()
            self._updated_screen()
            self.clock.tick(self.config.frame)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event: pygame.KEYDOWN) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event: pygame.KEYDOWN) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self) -> None:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _updated_screen(self):
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()
