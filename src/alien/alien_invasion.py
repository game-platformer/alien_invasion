import sys
from time import sleep

import pygame

from alien.alien import Alien
from alien.bullet import Bullet
from alien.button import Button
from alien.game_stats import GameStats
from alien.ship import Ship
from config.configuration import Configuration


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.config = Configuration()

        self.screen = pygame.display.set_mode((1024, 986))
        self.config.screen_height = self.screen.get_height()
        self.config.screen_width = self.screen.get_width()

        pygame.display.set_caption('Alien Invasion')
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = False
        self.play_button = Button(self, 'Play')

        self.clock = pygame.time.Clock()

    def run_game(self):
        running = True
        while running:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._updated_screen()
            self.clock.tick(self.config.frame)

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._chek_play_button(mouse_pos)

    def _chek_play_button(self, mouse_pos: tuple) -> None:
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.config.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

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
        if len(self.bullets) < self.config.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_aliens(self) -> None:
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_bullets(self) -> None:
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.config.increase_speed()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.config.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self) -> None:
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < (self.config.screen_height - 3 * alien_height):
            while current_x < (self.config.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position: int, y_position: int) -> None:
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self) -> None:
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        for alien in self.aliens.sprites():
            alien.rect.y += self.config.fleet_drop_speed
        self.config.fleet_direction *= -1

    def _updated_screen(self):
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()

        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()
