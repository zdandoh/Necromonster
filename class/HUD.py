import pygame
from os.path import join
from itertools import cycle
from ast import literal_eval


class HUD():
    def __init__(self, game):
        self.game = game

        #chat bar setup
        self.chat_active = 0
        self.chat_message = ''
        self.chat_toggle = cycle(reversed(range(2)))
        self.chat_bar = pygame.Surface([850, 20])
        self.chat_bar.fill((32, 32, 32))
        self.chat_bar.set_alpha(201)

        self.xpbar = pygame.image.load(join(self.game.main_path, 'rec', 'gui', 'xpbar.png')).convert_alpha()
        self.hpbar = pygame.image.load(join(self.game.main_path, 'rec', 'gui', 'hpbar.png')).convert_alpha()

        self.items = ['adamantium', 'mythril', 'iron_ingot']
        self.monsters = ['goop']


    def command(self, obj, pos, amount=1):
        position = literal_eval(pos)
        try:
            amnt = int(amount)
        except:
            pass
        
        if obj in self.items:
            for _ in xrange(amnt):
                self.game.Item(self.game, obj, [position[0], position[1]], world=1)
        elif obj in self.monsters:
            for _ in xrange(amnt):
                self.game.Monster(self.game, obj, [position[0], position[1]], 3, 'aggressive')
        else:
            pass
    
    def blitHUD(self):
        #hp bar creation
        blit_surface = pygame.Surface((abs(392 * (float(self.game.Player.stats['hp']) / self.game.Player.stats['maxhp'])), 24), pygame.SRCALPHA)
        blit_surface.fill((234, 0, 0, 213))
        self.game.screen.blit(blit_surface, (254, 589))

        #xp bar(s)
        blit_surface = pygame.Surface((497 * (float(self.game.Player.stats['mxp']) / self.game.Player.stats['maxmxp']), 12), pygame.SRCALPHA)
        blit_surface.fill((72, 196, 19, 221))
        self.game.screen.blit(blit_surface, (201, 636))
        blit_surface = pygame.Surface((497 * (float(self.game.Player.stats['pxp']) / self.game.Player.stats['maxpxp']), 12), pygame.SRCALPHA)
        blit_surface.fill((229, 102, 18, 221))
        self.game.screen.blit(blit_surface, (201, 622))

        self.game.screen.blit(self.xpbar, [200, 636])
        self.game.screen.blit(self.xpbar, [200, 622])
        self.game.screen.blit(self.hpbar, [250, 585])

        if self.chat_active:
            #blit the chat bar
            self.game.screen.blit(self.chat_bar, (25, 625))
            self.game.screen.blit(self.game.default_font.render(self.chat_message, True, (255, 255, 255)), [30, 628])
