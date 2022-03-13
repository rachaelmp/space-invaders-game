import os


class GameStats:

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.reset_stats()
        self.ships_left = self.settings.ship_limit
        self.last_ships_left = self.ships_left
        self.score = 0
        self.last_score = 0
        self.level = 0
        self.high_score = self.load_high_score()

    def __del__(self): self.save_high_score()

    def load_high_score(self):
        try:
            with open("stats/highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        try:
            with open("stats/highscore.txt", "w+") as f:
                f.write(str(round(self.highscore, -1)))
        except:
            print("highscore.txt not found...")

    def get_score(self):
        return self.score

    def get_lastscore(self):
        return self.last_score

    def get_highscore(self):
        return self.high_score

    def get_level(self):
        return self.level

    def get_ships_left(self):
        return self.ships_left

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.settings.reset_difficulty()

    def level_up(self): 
        self.level += 1
        self.settings.increase_difficulty(1)
        print("leveling up: level is now ", self.level)

    def alien_hit(self, alien):
        self.score += alien.points
        self.high_score = max(self.score, self.high_score)

    def ship_hit(self):
        self.ships_left -= 1
        n = self.ships_left
        print(f'SHIP HIT!', end=' ')
        if self.last_ships_left != self.ships_left:
            print(f'{self.ships_left} ship{"s" if n != 1 else ""} left')
            self.last_ships_left = self.ships_left


def load_high_score():
    try:
        with open("stats/highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0
