import pygame as pg
import alien
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import Timer
from sound import Sound


class Lasers:

    def __init__(self, game, owner):

        self.game = game
        self.stats = game.stats
        self.sound = game.sound
        self.owner = owner
        self.alien_fleet = game.alien_fleet
        self.lasers = Group()

    def add(self, laser): self.lasers.add(laser)

    def empty(self): self.lasers.empty()

    def fire(self): 
        new_laser = Laser(self.game, owner=self.owner)
        self.lasers.add(new_laser)
        snd = self.sound
        snd.play_pop() if type(self.owner) is alien.AlienFleet else snd.play_bubble()

    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        collisions = pg.sprite.groupcollide(self.alien_fleet.fleet, self.lasers, False, True)
        for alien in collisions: 
            if not alien.dying:
                alien.hit()

        if self.alien_fleet.length() == 0:
            self.stats.level_up()
            self.game.restart()
            
        for laser in self.lasers:
            laser.update(laser)

    def draw(self):
        for laser in self.lasers:
            laser.draw()


class Laser(Sprite):
    firing_images = [pg.image.load(f'images/bubble_{n}.png') for n in range(4)]

    def __init__(self, game, owner):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship
        self.alien_fleet = game.alien_fleet
        self.owner = owner

        self.image = pg.image.load('images/bubble_0.png')
        self.rect = self.image.get_rect()
        self.center = copy(self.ship.center)
        # print(f'center is at {self.center}')
        self.v = Vector(0, -1) * self.settings.laser_speed_factor

        self.normal_timer = Timer(image_list=Laser.firing_images, delay=100, is_loop=True)
        self.timer = self.normal_timer

    def update(self, owner):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x - 16, self.rect.y - 32
        self.screen.blit(image, rect)
