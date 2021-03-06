import sys
import os

sys.path.append('class')

import pygame
from pygame.locals import *

# class imports from rec\class
import mapLoader
from Entity import Entity
from EntityHandler import EntityHandler
from scheduler import Schedule
from player import Player
from monster import Monster
from npc import NPC, NPCText
from items import Item
from inventory import Invent
from HUD import HUD
from projectile import Projectile
from equipment import Weapon, Garment
from particle import *

pygame.init()


class Necro():
    def __init__(self):
        """
        Main game class initialization. All other class references point to this class as "game"
        """
        # window setup
        pygame.display.set_caption('Necromonster')
        pygame.display.set_icon(pygame.image.load(os.path.join('rec', 'misc', 'icon.png')))
        self.main_path = os.getcwd()

        # initiate the clock and screen object
        self.clock = pygame.time.Clock()
        self.FPS = 50
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [900, 650]
        self.center_point = [470, 350]
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        #DEBUG values
        self.DEBUG = 1
        self.RECT_DEBUG = 0
        self.angle = 0

        #Init and assign custom game class(es)
        self.EntityHandler = EntityHandler(self)
        self.ParticleManager = ParticleManager(self)
        self.Scheduler = Schedule(self)
        self.Entity = Entity
        self.Projectile = Projectile
        self.Monster = Monster
        self.NPC = NPC
        self.NPCText = NPCText
        self.Item = Item
        self.Inventory = Invent
        self.Invent = self.Inventory(self)
        self.Weapon = Weapon
        self.Garment = Garment
        self.Player = Player(self)
        self.HUD = HUD(self)

        # Init entity manager vars
        self.entities = []
        self.shadows = []

        # load fonts, create font list
        # do not use pygame.font.SysFont!
        self.text_list = []
        self.default_font = pygame.font.Font(os.path.join('rec', 'font', 'freesansbold.ttf'), 15)
        self.speak_font = pygame.font.Font(os.path.join('rec', 'font', 'freesansbold.ttf'), 30)

        # load the map that player is on
        self.INSIDE = 0
        self.blit_list = mapLoader.load('home', self)

        # spawn initial map items/entities
        self.Item(self, 'Mythril', [350, 400], world=1)
        self.NPC(self, "blacksmith", [400, 400], 100, 'still')
        for i in xrange(4):
            self.Monster(self, 'chicken', [200+(i*50),650], 1, 'neutral')
        self.Monster(self, "goop", [100, 100], 1, 'aggressive')

        # begin main game loop
        while 1:
            self.Loop()

    def Loop(self):
        """
        Main loop of the game. Calls tick, draw, and event processing
        functions. Tick and draw are only called every 20 milliseconds
        """
        self.eventLoop()
        self.Tick()
        self.Draw()
        pygame.display.update()

    def eventLoop(self):
        """
        Uses pygame event handling to process keypresses and mouse clicks.
        Used for chat, interacting with objects, and inventory management
        """
        for event in pygame.event.get():
            event # prevents exit button freeze up
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # toggle chat bar active
                if not self.HUD.chat_active:
                    if event.key == K_e:
                        self.Invent.toggleView()
                    if event.key == K_t:
                        #activate the chat bar
                        self.HUD.chat_message = ''
                        self.HUD.chat_active = 1
                        self.Player.can_move = 0
                        return 0
                # process chat messages. Remove or add characters while chat box is open
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    self.HUD.processCommand(self.HUD.chat_message)
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
                # interaction with entities on space bar press
                if event.key == K_SPACE:
                    for monster in self.EntityHandler.monsters:
                        if monster.NPC:
                            if monster.isPlayerClose(75) and monster.interacting == False:
                                monster.interacting = True
                            elif not monster.isPlayerClose(75) or monster.interacting == True:
                                monster.interacting = False
                                self.HUD.delPrompt()
            # inventory management, checks for item throws, and placement in slots.
            elif event.type == MOUSEBUTTONDOWN:
                self.Invent.last_click = pygame.mouse.get_pos()
                if self.Invent.in_hand:
                    self.Invent.testThrow(self.Invent.last_click)
                if self.Invent.shown:
                    self.Invent.inventClick(self.Invent.last_click)
                elif pygame.mouse.get_pressed()[0]:
                    self.Player.attack(pygame.mouse.get_pos())

    def Tick(self):
        """
        Updates all game math and entity states. No drawing is done.
        """
        ttime = self.clock.tick(self.FPS)
        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[K_EQUALS]:
            self.HUD.daytime_start -= 3
        if self.keys_pressed[K_MINUS]:
            self.HUD.daytime_start += 3
        self.Scheduler.update()
        self.EntityHandler.updateAll(ttime)

        self.Invent.update()
        self.HUD.updateDay()
        for index, text in enumerate(self.text_list):
            if text[2]:
                raise DeprecationWarning
        self.last_tick = pygame.time.get_ticks()

    def off(self, coords):
        """
        Offsets image coordinates to appear correct from the view of the player.
        Should be called on all surface coordinates before blitting.
        """
        newx = coords[0] - self.Player.player_r.x + 450
        newy = coords[1] - self.Player.player_r.y + 325
        return [newx, newy]

    def unoff(self, coords):
        """
        Removes the offset created by the off() function.
        """
        newx = coords[0] + self.Player.player_r.x - 450
        newy = coords[1] + self.Player.player_r.y - 325
        return [newx, newy]

    def getCenterBlit(self, surface, pos):
        pos[0] = pos[0] + surface.get_width() / 2
        pos[1] = pos[1] + surface.get_height() / 2
        return pos

    def rotopoint(self, surface, angle, pos):
        size = surface.get_size()
        if pos[0] > size[0]/2 or pos[1] > size[1]/2:
            print 'BIG ASS HONKEY'
        new_surf_size = [(size[0] - pos[0])*2, (size[1] - pos[1])*2]
        new_surf_blit_pos = [new_surf_size[0] - size[0], new_surf_size[1] - size[1]]
        new_surf = pygame.Surface(new_surf_size, pygame.SRCALPHA, 32)
        new_surf.blit(surface, new_surf_blit_pos)
        return pygame.transform.rotate(new_surf, angle)

    def testrot(self, image, angle):
        loc = image.get_rect().center
        new_rot = pygame.transform.rotate(image, angle)
        new_rot.get_rect(center=loc)
        return new_rot, new_rot.get_rect()


    def Draw(self):
        """
        Completes all blitting to the screend object, includes HUD updates.
        """
        tile_width = self.tile[1][0]
        tile_height = self.tile[1][1]
        tile_extrax = self.Player.player_r.x % tile_width
        tile_extray = self.Player.player_r.y % tile_height
        y = 0

        for i in xrange(self.screen_res[1] / tile_height + 3):
            for i in xrange(self.screen_res[0] / tile_width + 3):
                self.screen.blit(self.tile[0], [i * tile_width - tile_width - tile_extrax, y - tile_height - tile_extray])
            y += self.tile[1][1]
        if self.shadows:
            for s in self.shadows:
                s.update(self.screen)
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
        #Draws player and head text if it exists
        if self.Player.head_drawn:
            if self.Player.head_drawn[3]:
                self.screen.blit(self.Player.head_drawn[0], self.Player.head_drawn[1])
            else:
                self.Player.game.screen.blit(self.Player.head_drawn[0], self.off(self.Player.head_drawn[1]))
        self.ParticleManager.update()
        if self.Player.map_change:
            self.HUD.updateMapTrans()
        self.HUD.blitHUD()
Necro()
