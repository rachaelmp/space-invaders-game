import pygame as pg
import sys
from alien import AlienFleet, Alien
from vector import Vector
from button import Button
from game_settings import Settings
from sound import Sound

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)
PINK = (200, 100, 120)
BLUE = (100, 150, 200)
DARK_BLUE = (10, 10, 30)


class LandingPage:
    alien1_imgs = [pg.image.load(f'images/alien-1_{n}.png') for n in range(4)]
    alien2_imgs = [pg.image.load(f'images/alien-2_{n}.png') for n in range(4)]
    alien3_imgs = [pg.image.load(f'images/alien-3_{n}.png') for n in range(4)]
    alien4_imgs = [pg.image.load(f'images/alien-4_{n}.png') for n in range(4)]

    def __init__(self, game):
        self.screen = game.screen
        self.landing_page_finished = False
        self.stats = game.stats
        self.sound = game.sound

        heading_font = pg.font.SysFont(None, 192)
        subheading_font = pg.font.SysFont(None, 122)
        font = pg.font.SysFont(None, 48)

        strings = [('', BLUE, heading_font), ('', PINK, subheading_font),
                   ('= 10 PTS', BLUE, font), ('= 20 PTS', BLUE, font),
                   ('= 50 PTS', PINK, font), ('= 500 PTS', PINK, font),
                   ('HIGH SCORE = ' + str(self.stats.high_score), BLUE, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        alien = [100 * x + 300 for x in range(4)]
        # play_high = [x for x in range(650, 760, 80)]
        # play_high = 730
        self.posns.extend(alien)
        self.posns.append(730)

        centerx = self.screen.get_rect().centerx

        self.play_button = Button(self.screen, "PLAY GAME", ul=(centerx - 150, 650))

        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        self.alien1 = Alien(game=game, image_list=LandingPage.alien1_imgs, sound=self.sound, alien_index=0,
                            v=Vector(), ul=(centerx - 180, 250))
        self.alien2 = Alien(game=game, image_list=LandingPage.alien2_imgs, sound=self.sound, alien_index=1,
                            v=Vector(), ul=(centerx - 180, 350))
        self.alien3 = Alien(game=game, image_list=LandingPage.alien3_imgs, sound=self.sound, alien_index=2,
                            v=Vector(), ul=(centerx - 180, 450))
        self.alien4 = Alien(game=game, image_list=LandingPage.alien4_imgs, sound=self.sound, alien_index=3,
                            v=Vector(), ul=(centerx - 180, 550))

        self.hover = False

    def get_text(self, font, msg, color): return font.render(msg, True, color, DARK_BLUE)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def mouse_on_button(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.play_button.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:   # pretend PLAY BUTTON pressed
                self.landing_page_finished = True        
            elif e.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_x, mouse_y):
                    self.landing_page_finished = True
            elif e.type == pg.MOUSEMOTION:
                if self.mouse_on_button() and not self.hover:
                    self.play_button.toggle_colors()
                    self.hover = True
                elif not self.mouse_on_button() and self.hover:
                    self.play_button.toggle_colors()
                    self.hover = False

    def update(self):       # TODO make aliens move
        pass 

    def show(self):
        while not self.landing_page_finished:
            self.update()
            self.draw()
            self.check_events()   # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw_background(self):
        background_img = pg.image.load(f'images/background.png')
        logo_img = pg.image.load(f'images/logo.png')
        self.screen.blit(background_img, (0, 0))
        self.screen.blit(logo_img, (420, 50))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_background()
        self.alien1.draw()
        self.alien2.draw()
        self.alien3.draw()
        self.alien4.draw()
        self.draw_text()
        self.play_button.draw()
        # self.alien_fleet.draw()   # TODO draw my aliens
        # self.lasers.draw()        # TODO dray my button and handle mouse events
        pg.display.flip()
