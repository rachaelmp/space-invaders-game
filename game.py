import pygame as pg
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from game_stats import GameStats
from laser import Lasers
from ship import Ship
from alien import AlienFleet
from game_settings import Settings
from scoreboard import ScoreBoard
from game_over_page import GameOverPage
from sound import Sound
from barrier import Barriers


class Game:
    RED = (255, 0, 0)

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = GameStats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.sound = Sound()
        self.sb = ScoreBoard(game=self)
        self.game_over_page = GameOverPage(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.lasers = Lasers(game=self, owner=self.ship)
        self.alien_lasers = Lasers(game=self, owner=self.alien_fleet)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)
        self.alien_fleet.set_alien_lasers(self.alien_lasers)
        self.finished = False
        # self.barriers = Barriers(game=self)

    def restart(self):
        print("restarting the game")
        while self.sound.busy():
            pass
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.sb.update()
        self.game_over_page.update()
        # self.barriers.update()

    def draw(self):

        self.screen.fill(self.bg_color)
        background_img = pg.image.load(f'images/background.png').convert()
        self.screen.blit(background_img, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.sb.draw()
        # self.barriers.draw()

        pg.display.flip()

    def bgm(self):
        if self.stats.level > 1:
            self.sound.play_very_fast_bg()
        self.sound.play_bg()

    def play(self):
        self.finished = False
        self.bgm()
        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)

        self.game_over()
        sleep(0.5)

    def game_over(self):
        print('\nGAME OVER!\n')
        print('Final Score: ', self.stats.score, '\n\n')

    def reset(self):
        print('resetting...')
        self.stats.reset_stats()


def main():
    g = Game()
    lp = LandingPage(game=g)
    gop = GameOverPage(game=g)
    lp.show()

    while gop.will_restart:
        g.reset()
        g.play()
        gop.show()


if __name__ == '__main__':
    main()
