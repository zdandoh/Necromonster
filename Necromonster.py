import sys
import os
sys.path.append('class')

import pygame
from pygame.locals import *

import mapLoader
from player import Player
from monster import Monster
from items import Item
from inventory import Invent
from HUD import HUD
from projectile import Projectile

pygame.init()

class Necro():
    def __init__(self):
        #window setup
        pygame.display.set_caption('Necromonster')
        pygame.display.set_icon(pygame.image.load(os.path.join('rec', 'misc', 'icon.png')))
        self.main_path = os.getcwd()

        # initiate the clock and screen
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [900, 650]
        self.center_point = [470., 350.]
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.DEBUG = 1

        #Init custom game classes
        self.Projectile = Projectile
        self.Player = Player(self)
        self.Monster = Monster(self)
        self.ItemHandler = Item(self)
        self.Invent = Invent(self)
        self.HUD = HUD(self)

        # load fonts, create font list
        self.text_list = []
        self.default_font = pygame.font.SysFont(None, 20)

        # get the map that you are on
        self.blit_list = mapLoader.load('home', self)

        self.Monster.create('goop', [300, 300], 2, 'neutral')

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
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    self.Invent.toggleView()
            elif event.type == MOUSEBUTTONDOWN:
                if self.Invent.in_hand:
                    self.Invent.testThrow(pygame.mouse.get_pos())
                if self.Invent.shown:
                    self.Invent.inventClick(pygame.mouse.get_pos())
                elif pygame.mouse.get_pressed()[0]:
                    self.Player.attack(pygame.mouse.get_pos())

    def Tick(self):
        # updates to player location and animation frame
        self.keys_pressed = pygame.key.get_pressed()
        self.clock.tick()
        self.Player.update()
        self.Monster.update()
        self.ItemHandler.update()
        self.Invent.update()
        for index, text in enumerate(self.text_list):
            if text[2] < time():
                self.text_list.pop(index)

        self.last_tick = pygame.time.get_ticks()

    def off(self, coords):
        newx = coords[0] - self.Player.player_r.x + 450
        newy = coords[1] - self.Player.player_r.y + 325
        return [newx, newy]

    def Draw(self):
        #Responsible for calling all functions that draw to the screen
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
                self.Monster.blitMonsters()
            else:
                self.screen.blit(surf[0], self.off(surf[1]))
        for text in self.text_list:
            self.screen.blit(text[0], text[1])
        self.ItemHandler.blitItems()
        if self.Invent.shown:
            self.Invent.draw()
        if self.DEBUG:
            self.screen.blit(self.default_font.render(str(round(self.clock.get_fps())), True, (255, 255, 255)), [0, 0])
            self.screen.blit(self.default_font.render(str('%s, %s' % (self.Player.player_r.x, self.Player.player_r.y)), True, (255, 255, 255)), [0, 12])
            self.screen.blit(self.default_font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255)), [0, 24])

        self.HUD.blitHUD()
Necro()
