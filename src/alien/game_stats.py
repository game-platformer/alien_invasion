from alien import alien_invasion as Alien


class GameStats:
    def __init__(self, ai_game: Alien):
        self.config = ai_game.config
        self.ships_left = 0

        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.config.ship_limit
