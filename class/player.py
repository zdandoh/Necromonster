import pygame
from pygame.locals import *

import mapLoader

import math
import os
from ast import literal_eval

class Player():
    def __init__(self, game):
        self.game = game
        self.player = pygame.image.load(os.path.join('rec', 'char', 'back1.png'))
        self.head_font = pygame.font.Font(os.path.join('rec', 'font', 'p_head.ttf'), 15)
        self.can_move = 1
        self.knocked = 0
        self.player_face = 'back'  # this is the part of the player that you see
        self.player_state = 1.
        self.head_drawn = 0
        self.player_r = self.player.get_rect()
        self.player_dims = self.player.get_size()

        # setup attack vars
        self.last_attack = pygame.time.get_ticks()

        self.player_frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'char')):
            if fi.endswith('.png'):
                self.player_frames[fi] = pygame.image.load(os.path.join(self.game.main_path, 'rec', 'char', fi)).convert_alpha()

        self.player_r.x = 450
        self.player_r.y = 650

        # stats
        self.stats = {}
        self.stats['hp'] = 10
        self.stats['maxhp'] = 10
        self.stats['maxpxp'] = 1000
        self.stats['maxmxp'] = 1000
        self.stats['pxp'] = 312
        self.stats['mxp'] = 654
        self.stats['attack'] = 5
        self.stats['defense'] = 3
        self.weapon = self.game.Weapon('wand', self.game)
        self.speed = 250

    def update(self, ttime):
        #Update player position based on keypresses
        if 1 in self.game.keys_pressed and self.can_move:
            if self.game.keys_pressed[K_w]:
                self.player_r.y += -2
                self.onMove([0, -2])
                self.player_face = 'back'
            if self.game.keys_pressed[K_a]:
                self.player_r.x += -2
                self.onMove([-2, 0])
                self.player_face = 'left'
            if self.game.keys_pressed[K_s]:
                self.player_r.y += 2
                self.onMove([0, 2])
                self.player_face = 'front'
            if self.game.keys_pressed[K_d]:
                self.player_r.x += 2
                self.onMove([2, 0])
                self.player_face = 'right'

            self.player_state += 0.15
            if self.player_state >= 4.:
                self.player_state = 1.
        if not self.game.keys_pressed[K_w] and not self.game.keys_pressed[K_a] and not self.game.keys_pressed[K_s] and not self.game.keys_pressed[K_d] and self.can_move:
            self.player_state = 1.
        self.player = self.player_frames['%s%s.png' % (self.player_face, int(self.player_state))]

        if self.weapon.shown == 1:
            self.weapon.blit()

    def onMove(self, offset, link_count = 0):
        #Collision detection run on movement
        m_rects = [x.rect for x in self.game.EntityHandler.monsters]
        if self.player_r.x > self.game.Grid.bounds[0] or self.player_r.x <= 0:
            self.player_r.x -= offset[0]
        if self.player_r.y > self.game.Grid.bounds[1] or self.player_r.y <= 0:
            self.player_r.y -= offset[1]
        for rect in self.game.solid_list + m_rects:
            link_active = 0
            if 'LINK' in rect:
                link = self.game.links[link_count]
                rect = literal_eval(link[1])
                link_count += 1
                link_active = 1
            if self.player_r.colliderect(rect):
                if link_active:
                    self.game.blit_list = mapLoader.load(link[2], self.game, new_pos = link[3], face = link[4])
                else:
                    self.player_r.y -= offset[1]
                    self.player_r.x -= offset[0]

    def getDegrees(self, mpos):
        ppos = self.game.center_point
        mpos = pygame.mouse.get_pos()
        try:
            degrees = math.degrees(math.atan((mpos[0] - ppos[0]) / (mpos[1] - ppos[1])))
        except ZeroDivisionError:
            degrees = 0
        if not degrees:
            if mpos[1] == ppos[1] or mpos[0] == ppos[0]:
                if mpos[0] > ppos[0]:
                    degrees = 90
                elif mpos[0] < ppos[0]:
                    degrees = 270
                elif mpos[1] > ppos[1]:
                    degrees = 180
                elif mpos[1] > ppos[1]:
                    degrees = 0

        elif mpos[0] > ppos[0] and mpos[1] < ppos[1]:
            degrees = abs(degrees)
        elif mpos[0] > ppos[0] and mpos[1] > ppos[1]:
            degrees = 90 - degrees + 90
        elif mpos[0] < ppos[0] and mpos[1] > ppos[1]:
            degrees = abs(degrees) + 180
        elif mpos[0] < ppos[0] and mpos[1] < ppos[1]:
            degrees = 90 - degrees + 270
        else:
            raise Exception('Incalculable degrees %s' % degrees)
        return int(360 - degrees)

    def takeOver(self, monster):
        #replace all player stats and frames with monster
        self.stats['hp'] = int(monster.hp)
        self.stats['maxhp'] = int(monster.maxhp)
        self.stats['attack'] = int(monster.attack)
        self.stats['defense'] = int(monster.defense)
        self.stats['speed'] = int(monster.speed)

        self.weapon = self.game.Weapon(monster.weapon, self.game)
        self.player = monster.frames['front1.png']
        self.player_frames = monster.frames

    def headDraw(self, text, dur=3):
        #Draw text at head of player(s)
        font_render = self.head_font.render(text, True, (255, 255, 255))
        self.head_drawn = [font_render, self.game.off([self.player_r.x - font_render.get_size()[0] / 2 + self.player_dims[0] / 2, self.player_r.y - 25]), pygame.time.get_ticks() + dur]
        self.game.Scheduler.add('self.game.Player.head_drawn = ""', dur * 1000)

    def addPos(self, move):
        self.player_r.x += move[0]
        self.player_r.y += move[1]

    def move(self, change):
        self.addPos(change)
        self.onMove(change)

    def collides(self, rect):
        return self.player_r.colliderect(rect)

    def setPos(self, new):
        self.player_r.x = new[0]
        self.player_r.y = new[1]

    def getRect(self):
        return Rect(self.player_r)

    def getPos(self, offset=[0, 0]):
        return [self.player_r.x + offset[0], self.player_r.y + offset[1]]

    def getNode(self):
        return (self.player_r.x + 20) / 10, (self.player_r.y + 30) / 10

    def getDistance(self, rect):
        return math.hypot(self.player_r.x - rect.x, self.player_r.y - rect.y)

    def setFace(self, face, state=1):
        face = face.replace('\r', '')
        if face:
            self.player_face = face

    def attack(self, mpos):
        # (y - y) / (x - x)
        degrees = 360 - self.getDegrees(mpos)
        if 135 > degrees >= 45:
            self.setFace('right')
        elif 225 > degrees >= 135:
            self.setFace('front')
        elif 315 > degrees >= 225:
            self.setFace('left')
        else:
            self.setFace('back')
        speed = 4.
        range = 200
        distance = [mpos[0] - self.game.center_point[0], mpos[1] - self.game.center_point[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]

        self.weapon.onClick(self.game, bullet_vector)

    def takeDamage(self, damage):
        damage -= self.stats['defense']
        if self.stats['hp'] > 0:
            if damage <= 0:
                damage = 1
            self.stats['hp'] -= damage

    def blitPlayer(self):
        #Draws player and head text if it exists
        if self.head_drawn:
            self.game.screen.blit(self.head_drawn[0], self.head_drawn[1])
        self.game.screen.blit(self.player, self.game.off([self.player_r.x, self.player_r.y]))
