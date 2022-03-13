import pygame as pg
import sys
from alien import AlienFleet, Alien
# from settings import Settings
from vector import Vector
from button import Button
from sound import Sound

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)
PINK = (200, 100, 120)
BLUE = (100, 150, 200)
DARK_BLUE = (10, 10, 30)


class GameOverPage:

    def __init__(self, game):
        self.screen = game.screen
        self.game_over_page_finished = False
        self.stats = game.stats
        self.sound = game.sound

        self.score = self.stats.score
        self.high_score = self.stats.high_score

        headingFont = pg.font.SysFont(None, 192)
        subheadingFont = pg.font.SysFont(None, 122)
        font = pg.font.SysFont(None, 48)

        strings = [('GAME', BLUE, headingFont), ('OVER', PINK, subheadingFont),]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        self.posns.append(600)
        self.posns.append(650)

        centerx = self.screen.get_rect().centerx

        self.restart_button = Button(self.screen, "RESTART", ul=(500, 350))
        self.quit_button = Button(self.screen, "QUIT", ul=(500, 450))

        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]

        self.hover_restart = False
        self.hover_quit = False
        self.will_restart = True

    def get_text(self, font, msg, color): return font.render(msg, True, color, DARK_BLUE)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def mouse_on_restart_button(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.restart_button.rect.collidepoint(mouse_x, mouse_y)

    def mouse_on_quit_button(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.quit_button.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:
                self.game_over_page_finished = True
            elif e.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.restart_button.rect.collidepoint(mouse_x, mouse_y):
                    self.will_restart = True
                    self.game_over_page_finished = True
                elif self.quit_button.rect.collidepoint(mouse_x, mouse_y):
                    self.will_restart = False
                    self.game_over_page_finished = True
                    sys.exit()
            elif e.type == pg.MOUSEMOTION:
                if self.mouse_on_restart_button() and not self.hover_restart:
                    self.restart_button.toggle_colors()
                    self.hover_restart = True
                elif not self.mouse_on_restart_button() and self.hover_restart:
                    self.restart_button.toggle_colors()
                    self.hover_restart = False
                elif self.mouse_on_quit_button() and not self.hover_quit:
                    self.quit_button.toggle_colors()
                    self.hover_quit = True
                elif not self.mouse_on_quit_button() and self.hover_quit:
                    self.quit_button.toggle_colors()
                    self.hover_quit = False

    def update(self):
        self.score = self.stats.score
        self.high_score = self.stats.high_score

    def show(self):
        self.sound.play_game_over()
        while not self.game_over_page_finished:
            self.update()
            self.draw()
            self.check_events()   # exits game if QUIT pressed
        self.game_over_page_finished = False

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw_background(self):
        background_img = pg.image.load(f'images/background.png')
        self.screen.blit(background_img, (0, 0))

    def draw_scores(self):
        font = pg.font.SysFont(None, 48)
        scoretext = [('YOUR SCORE = ' + str(self.score), BLUE, font),
                     ('HIGH SCORE = ' + str(self.high_score), PINK, font)]

        n = len(scoretext)

        scoretexts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in scoretext]
        scorerects = [self.get_text_rect(text=scoretexts[i], centerx=600, centery=(600 + 50 * i)) for i in range(n)]

        for i in range(n):
            self.screen.blit(scoretexts[i], scorerects[i])



    def draw(self):
        self.screen.fill(BLACK)
        self.draw_background()
        self.draw_text()
        self.draw_scores()
        self.restart_button.draw()
        self.quit_button.draw()
        pg.display.flip()
