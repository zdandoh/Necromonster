import pygame
from os.path import join
import os
from itertools import cycle
from ast import literal_eval


class HUD():
    def __init__(self, game):
        self.game = game

        #chat bar setup
        self.chat_active = 0
        self.text_active = False
        self.prompt_result = 0
        self.chat_message = ''
        self.chat_toggle = cycle(reversed(range(2)))
        self.chat_bar = pygame.Surface([850, 20])
        self.chat_bar.fill((32, 32, 32))
        self.chat_bar.set_alpha(201)

        self.xpbar = pygame.image.load(join(self.game.main_path, 'rec', 'gui', 'xpbar.png')).convert_alpha()
        self.hpbar = pygame.image.load(join(self.game.main_path, 'rec', 'gui', 'hpbar.png')).convert_alpha()
        self.text_box = pygame.image.load(join(self.game.main_path, 'rec', 'gui', 'text_box.png')).convert_alpha()

        self.items = [f.split('.')[0] for f in os.listdir(join(self.game.main_path, 'rec', 'items'))]
        self.monsters = os.listdir(join(self.game.main_path, 'rec', 'enemy'))

    def command(self, obj, pos, amount=1):
        try:
            position = literal_eval(pos)
            amnt = int(amount)
            
            if obj in self.items:
                for _ in xrange(amnt):
                    self.game.Item(self.game, obj, [position[0], position[1]], world=1)
            elif obj in self.monsters:
                for _ in xrange(amnt):
                    self.game.Monster(self.game, obj, [position[0], position[1]], 3, 'aggressive')
            else:
                pass
        except:
            print "Invalid Command!"

    def makePrompt(self, npc_text):
        self.text_active = []
        main_text = npc_text.getText(npc_text.current_branch)
        main_render = self.game.speak_font.render(main_text, True, (0, 0, 0))
        self.text_active.append(main_render)
        options = npc_text.getOptions(npc_text.current_branch)
        for op_no, option in enumerate(options):
            if npc_text.getLabel(option):
                option_text = str(op_no + 1) + ': ' + npc_text.getLabel(option)
                option_render = self.game.speak_font.render(option_text, True, (0, 0, 0))
                self.text_active.append(option_render)

    def showPrompt(self):
        text_pos = [210, 120]
        first_text = self.text_active.pop(0)
        self.game.screen.blit(first_text, text_pos)
        for text in self.text_active:
            text_pos[1] += first_text.get_rect().height 
            self.game.screen.blit(text, text_pos)

    
    def blitHUD(self):
        #hp bar creation
        blit_surface = pygame.Surface((abs(392 * (float(self.game.Player.stats['hp']) / self.game.Player.stats['maxhp'])), 24), pygame.SRCALPHA)
        blit_surface.fill((234, 0, 0, 213))
        self.game.screen.blit(blit_surface, (254, 589))

        for monster in self.game.EntityHandler.monsters:
            if monster.NPC == True and monster.interacting == True:
                self.game.screen.blit(self.text_box, [170, 75])

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

        if self.text_active:
            self.showPrompt()