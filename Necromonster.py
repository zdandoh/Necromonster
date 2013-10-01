import sys
import os
import time
sys.path.append('class')

import pygame
from pygame.locals import *

import mapLoader
from EntityHandler import EntityHandler
from scheduler import Schedule
from player import Player
from monster import Monster
from items import Item
from inventory import Invent
from HUD import HUD
from projectile import Projectile
from weapons import Weapon

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

        #DEBUG values
        self.DEBUG = 1
        self.RECT_DEBUG = 0

        #Init custom game classe(s)
        self.EntityHandler = EntityHandler(self)
        self.Scheduler = Schedule(self)
        self.Projectile = Projectile
        self.Monster = Monster
        self.Item = Item
        self.Weapon = Weapon
        self.Player = Player(self)
        self.Invent = Invent(self)
        self.HUD = HUD(self)

        # Init entity manager vars
        self.entities = []


        # load fonts, create font list
        self.text_list = []
        self.default_font = pygame.font.SysFont(None, 20)

        # get the map that you are on
        self.blit_list = mapLoader.load('home', self)

        self.Monster(self, 'goop', [300, 300], 3, 'aggressive')

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
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not self.HUD.chat_active:
                    if event.key == K_e:
                        self.Invent.toggleView()
                    if event.key == K_t:
                        #activate the chat bar
                        self.HUD.chat_message = ''
                        self.HUD.chat_active = 1
                        self.Player.can_move = 0
                        return 0
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    self.HUD.chat_active = 0
                    self.Player.can_move = 1
                    self.HUD.chat_message = ''
                elif event.key == K_BACKSPACE:
                    self.HUD.chat_message = self.HUD.chat_message[:-1]
                elif event.key <= 255:
                    char = chr(event.key)
                    if self.keys_pressed[K_LSHIFT] or self.keys_pressed[K_RSHIFT]:
                        char = char.upper()
                    self.HUD.chat_message += char
            elif event.type == MOUSEBUTTONDOWN:
                if self.Invent.in_hand:
                    self.Invent.testThrow(pygame.mouse.get_pos())
                if self.Invent.shown:
                    self.Invent.inventClick(pygame.mouse.get_pos())
                elif pygame.mouse.get_pressed()[0]:
                    self.Player.attack(pygame.mouse.get_pos())

    def Tick(self):
        # updates to player location and animation frame
        ttime = self.clock.tick()
        self.keys_pressed = pygame.key.get_pressed()
        self.Scheduler.update()
        self.EntityHandler.updateAll(ttime)
        self.Invent.update()
        for index, text in enumerate(self.text_list):
            if text[2]:
                raise DeprecationWarning
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
                self.EntityHandler.blitAll()
            else:
                self.screen.blit(surf[0], self.off(surf[1]))
        for text in self.text_list:
            self.screen.blit(text[0], text[1])
        if self.Invent.shown:
            self.Invent.draw()
        if self.DEBUG:
            self.screen.blit(self.default_font.render(str(round(self.clock.get_fps())), True, (255, 255, 255)), [0, 0])
            self.screen.blit(self.default_font.render(str('%s, %s' % (self.Player.player_r.x, self.Player.player_r.y)), True, (255, 255, 255)), [0, 12])
            self.screen.blit(self.default_font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255)), [0, 24])
        if self.RECT_DEBUG:
            ps = pygame.Surface(self.Player.player_dims)
            ps.fill([255, 0, 0])
            self.screen.blit(ps, self.off([self.Player.player_r.x, self.Player.player_r.y]))
        self.HUD.blitHUD()
Necro()
