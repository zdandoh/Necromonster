import pygame
from pygame.locals import *
import sys
from ast import literal_eval

sys.path.append('class')

import mapLoader

pygame.init()


class Player():
    def __init__(self, game):
        self.game = game
        self.player = pygame.image.load('rec/char/back1.png')
        self.player_face = 'back'  # this is the part of the player that you see
        self.player_state = 1.
        self.player_r = self.player.get_rect()

        self.player_r.x = 50
        self.player_r.y = 50

    def update(self):
        if 1 in self.game.keys_pressed:
            if self.game.keys_pressed[K_w]:
                self.player_r.y += -2
                self.onMove(1, -2)
                self.player_face = 'back'
            if self.game.keys_pressed[K_a]:
                self.player_r.x += -2
                self.onMove(0, -2)
                self.player_face = 'left'
            if self.game.keys_pressed[K_s]:
                self.player_r.y += 2
                self.onMove(1, 2)
                self.player_face = 'front'
            if self.game.keys_pressed[K_d]:
                self.player_r.x += 2
                self.onMove(0, 2)
                self.player_face = 'right'

            self.player_state += 0.15
            if self.player_state >= 4:
                self.player_state = 1
            self.player = pygame.image.load('rec/char/%s%s.png' % (self.player_face, int(self.player_state)))
        if not self.game.keys_pressed[K_w] and not self.game.keys_pressed[K_a] and not self.game.keys_pressed[K_s] and not self.game.keys_pressed[K_d]:
            self.player_state = 1

    def onMove(self, pos, offset, link_count = 0):
        for rect in self.game.solid_list:
            link_active = 0
            if 'LINK' in rect:
                link = self.game.links[link_count]
                rect = literal_eval(link[1])
                link_count += 1
                link_active = 1
            if self.player_r.colliderect(rect):
                if link_active:
                    print 'Link triggered'
                    self.game.blit_list = mapLoader.load(link[2], self.game, new_pos = link[3], face = link[4])
                else:
                    if pos:
                        self.player_r.y -= offset
                    elif not pos:
                        self.player_r.x -= offset

    def addPos(self, move):
        self.player_r.x += move[0]
        self.player_r.y += move[1]

    def setPos(self, new):
        self.player_r.x = new[0]
        self.player_r.y = new[1]

    def setFace(self, face, state=1):
        self.player_face = pygame.image.load('rec/char/%s%s.png' % (face, state))

    def blitPlayer(self):
        self.game.screen.blit(self.player, self.game.off([self.player_r.x, self.player_r.y]))


class Necro():
    def __init__(self):
        self.Player = Player(self)
        # initiate the clock and screen
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [900, 650]
        self.screen = pygame.display.set_mode(self.screen_res, 0, 32)
        self.DEBUG = 1

        # load fonts
        self.default_font = pygame.font.SysFont(None, 20)

        # get the map that you are on
        self.blit_list = mapLoader.load('inside', self)

        while 1:
            self.Loop()

    def Loop(self):
        # main game loop
        self.eventLoop()
        if pygame.time.get_ticks() - self.last_tick > 20:
            self.Tick()
            self.Draw()
        pygame.display.update()

    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

    def Tick(self):
        # updates to player location and animation frame
        self.keys_pressed = pygame.key.get_pressed()
        self.clock.tick()
        self.Player.update()

        self.last_tick = pygame.time.get_ticks()

    def off(self, coords):
        newx = coords[0] - self.Player.player_r.x + 450
        newx = coords[0] - self.Player.player_r.x + 450
        newy = coords[1] - self.Player.player_r.y + 325
        return [newx, newy]

    def Draw(self):
        tile_width = self.tile[1][0]
        tile_height = self.tile[1][1]
        tile_extrax = self.Player.player_r.x % tile_width
        tile_extray = self.Player.player_r.y % tile_height
        y = 0

        for i in xrange(self.screen_res[1] / tile_height + 3):
            for i in xrange(self.screen_res[0] / tile_width + 3):
                self.screen.blit(self.tile[0], [i * tile_width - tile_width - tile_extrax, y - tile_height - tile_extray])
            y += self.tile[1][1]
        for surf in self.blit_list:
            if 'player' in surf:
                self.Player.blitPlayer()
            else:
                self.screen.blit(surf[0], self.off(surf[1]))
        if self.DEBUG:
            self.screen.blit(self.default_font.render(str(self.clock.get_fps()), True, (255, 255, 255)), [0, 0])

Necro()