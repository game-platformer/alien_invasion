from dataclasses import dataclass


@dataclass
class Configuration:
    frame: int = 60
    bg_color: list = (230, 230, 230)
    screen_width: int = 1200
    screen_height: int = 800

    # imagen
    imagen_ship: str = 'assets/ship.bmp'

    # Ship
    ship_speed = 1.5
    ship_limit = 3

    # Bullet
    bullet_speed = 2.5
    bullet_width = 3
    bullet_height = 15
    bullet_color = (60, 60, 60)
    bullets_allowed = 3

    # Alien
    alien_speed = 3
    fleet_drop_speed = 10
    fleet_direction = 1

    # rapidez
    speedup_scale = 1.1

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
