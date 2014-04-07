import pathfind
import os
from random import randrange
from pygame.image import load
from pygame.draw import rect
from pygame.time import get_ticks


class Monster(object):
    def __init__(self, game, name, pos, difficulty, pathfinding):
        """
        Initializes monster class, sets all default values.
        """
        self.game = game
        self.name = name
        self.NPC = False
        self.frames = self.loadFrames(name)
        self.state = 1.
        self.path = pathfinding
        self.rect = self.frames.values()[0].get_rect()
        self.size = [self.rect.w, self.rect.h]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos
        self.movements = 0
        self.face = 'front'
        self.image = 0
        self.frameno = 1
        self.dead = 0
        self.riggings = {'front': [0, 0], 'back': [0, 0], 'left': [0, 0], 'right': [0, 0]}
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
        """
        Returns stats in format [level, health, attack, defense, speed, attacks per second, knockback]
        """
        return [difficulty, difficulty * 5, difficulty, difficulty, 3, 2, 10]

    def execInfo(self):
        """
        Execute the file info found in a monster's info.txt file. Should be moved over to a config.py system or something.
        """
        info = open(os.path.join('rec', 'entity', self.name, 'config.py')).read()
        exec(info)

    def getNode(self):
        """
        Gets the map node that the monster is in. Related to pathfinding.
        """
        self.node = self.rect.x / 10, self.rect.y / 10
        return self.node

    def setNode(self, node):
        """
        Set the node of the monster. Related to pathfinding.
        """
        self.node = self.getNode()
        self.rect.x = node[0] * 10
        self.rect.y = node[1] * 10

    def getPos(self):
        """
        Return monster position in [x, y] format.
        """
        return [self.rect.x, self.rect.y]

    def getDims(self):
        """
        Returns dimensions of a monster.
        """
        return [self.rect.w, self.rect.h]  # this is the proper return order

    def loadFrames(self, name):
        """
        Load all frames of a monster, filtering out those that do not end in .png
        Returns all frames as a list of surfaces.
        """
        frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'entity', name, 'img')):
            if '.png' in fi:
                frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'entity', name, 'img', fi)).convert_alpha()
        return frames

    def onDeath(self, index, drop=1):
        """
        Called when the monster dies. Drops loot.
        """
        if self.loot and drop == 1:
            self.game.Item(self.game, self.loot, pos=[self.rect.x, self.rect.y], spin=1, world=1)
        self.dead = 1

    def setRigging(self, front, back, left, right):
        """
        Set the rigging for each part of the monster.
        """
        self.riggings['front'] = front
        self.riggings['back'] = back
        self.riggings['left'] = left
        self.riggings['right'] = right

    def takeDamage(self, index, damage):
        """
        Does monster damage calculations. Takes into account defense.
        """
        try:
            damage += randrange(0, damage / 3)
        except ValueError:
            # empty randrange
            damage = 1
        damage -= self.defense
        if damage <= 0:
            damage = 1
        self.hp -= damage
        if self.hp <= 0:
            self.onDeath(index)

    def update(self, index, ttime):
        """
        Updates the state of the monster. Pathfinds and updates position, mainly.
        """
        self.state += 0.15
        if self.state >= 5.:
            self.player_state = 1.
        if not self.moving:
            self.state = 1.
        try:
            self.image = self.frames['%s%s.png' % (self.face, int(self.state))]
        except KeyError:
            # fix for takeover frame bug
            self.image = self.frames['%s%s.png' % (self.face, 3)]

        self.index = index
        if self.can_move == 1:
            getattr(pathfind, self.path)(self, self.game)
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y
        if self.dead:
            return 1

    def blit(self):
        """
        Responsible for drawing the current monster frame to the screen
        """
        if self.hp < self.maxhp:
            pos = [self.pos[0], self.pos[1] - self.size[1] / 2]
            rect(self.game.screen, (200, 50, 0), (self.game.off(pos), (self.size[0], 5)))
            rect(self.game.screen, (0, 200, 50), (self.game.off(pos), (self.size[0] * (self.hp / self.maxhp), 5)))

        self.game.screen.blit(self.image, self.game.off([self.rect.x, self.rect.y]))

