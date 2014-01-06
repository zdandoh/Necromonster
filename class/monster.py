import pathfind
import os
from random import randrange
from pygame.image import load
from pygame.draw import rect
from pygame.time import get_ticks


class Monster(object):
    def __init__(self, game, name, pos, difficulty, pathfinding):
        self.game = game
        self.name = name
        self.NPC = False
        self.frames = self.loadFrames(name)
        self.path = pathfinding
        self.rect = self.frames.values()[0].get_rect()
        self.size = [self.rect.w, self.rect.h]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos
        self.movements = 0
        self.face = 'front'
        self.frameno = 1
        self.dead = 0
        self.index = None
        self.last_attack = get_ticks()

        #parse info.txt file
        self.execInfo()

        # pathfinding vars
        self.movements = 0
        self.moving = '' # 1, 2, 3, 4; up, left, down, right
        self.can_move = 1
        self.path_found = 0
        self.initial_path = 1
        self.node = self.getNode()
        self.path_progress = []

        stats = self.getStats(difficulty)
        self.level = stats[0]
        self.hp = float(stats[1])
        self.maxhp = float(stats[1])
        self.attack = stats[2]
        self.defense = stats[3]
        self.speed = stats[4]
        self.aspeed = 1000. / stats[5]
        self.knockback = stats[6]
        self.loot = 'Iron Ingot'

        self.game.EntityHandler.monsters.append(self)

    def getStats(self, difficulty):
        # stat format [level, health, attack, defense, speed, attacks per second, knockback]
        return [difficulty, difficulty * 5, difficulty, difficulty, 3, 2, 10]

    def execInfo(self):
        info = open(os.path.join('rec', 'enemy', self.name, 'info.txt')).read()
        exec(info)

    def getNode(self):
        # gets the map node that the monster is in
        self.node = self.rect.x / 10, self.rect.y / 10
        return self.node

    def setNode(self, node):
        self.node = self.getNode()
        self.rect.x = node[0] * 10
        self.rect.y = node[1] * 10

    def getPos(self):
        return [self.rect.x, self.rect.y]

    def getDims(self):
        return [self.rect.w, self.rect.h]  # this is the proper return order

    def loadFrames(self, name):
        frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'enemy', name, 'img')):
            if '.png' in fi:
                frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'enemy', name, 'img', fi)).convert_alpha()
        return frames

    def onDeath(self, index, drop=1):
        if self.loot and drop == 1:
            self.game.Item(self.game, self.loot, pos=[self.rect.x, self.rect.y], spin=1, world=1)
        self.dead = 1

    def takeDamage(self, index, damage):
        damage += randrange(0, damage / 3)
        damage -= self.defense
        if damage <= 0:
            damage = 1
        self.hp -= damage
        if self.hp <= 0:
            self.onDeath(index)

    def update(self, index, ttime):
        self.index = index
        if self.can_move == 1:
            getattr(pathfind, self.path)(self, self.game)
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y
        if self.dead:
            return 1

    def blit(self):
        if self.hp < self.maxhp:
            pos = [self.pos[0], self.pos[1] - self.size[1] / 2]
            rect(self.game.screen, (200, 50, 0), (self.game.off(pos), (self.size[0], 5)))
            rect(self.game.screen, (0, 200, 50), (self.game.off(pos), (self.size[0] * (self.hp / self.maxhp), 5)))
        self.game.screen.blit(self.frames['%s%s.png' % (self.face, self.frameno)], self.game.off([self.rect.x, self.rect.y]))

