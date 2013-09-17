from pygame.image import load as img_load
from pygame.transform import rotate
import os

class Projectile():
    def __init__(self, game, name, vector, damage='def', pos='def', degrees=0):
        # general vars
        #assign defaults to a player attack
        if damage == 'def':
            damage = game.Player.stats['attack']
        if pos == 'def':
            pos = game.Player.getPos(offset=[20, 30])
        self.game = game
        self.degrees = degrees
        self.speed = 5
        self.vector = vector
        self.frames = self.loadFrames(name)
        self.turnFrames()
        self.frame = 0
        self.dims = list(self.frames[self.frame].get_size())
        self.rect = self.frames[self.frame].get_bounding_rect()
        self.range = range
        self.damage = damage
        self.dead = 0
        self.travelled = 0

        self.pos = [float(pos[0]) - (self.surf.get_size()[0] / 2), float(pos[1]) - (self.surf.get_size()[1])]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        #ranged update vars
        self.collides_with_player = 1
        #dagger update vars
        self.retracting = 0
        self.start_pos = self.pos

        self.load(name)
        self.game.EntityHandler.projectiles.append(self)

    def add(self):
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def loadFrames(self, name):
        frames = []
        for fi in os.listdir(os.path.join('rec', 'projectile', name)):
            if '.png' in fi:
                frames.append(img_load(os.path.join('rec', 'projectile', name, fi)))
        return frames

    def load(self, name):
        config_file = open(os.path.join('rec', 'projectile', name, 'config.py')).read()
        exec(config_file)
        self.frames = self.loadFrames(name)

    def sub(self, reps=1):
        for _ in xrange(reps):
            self.pos[0] -= self.vector[0]
            self.pos[1] -= self.vector[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def turnFrames(self):
        for frame in self.frames:
            self.surf = rotate(frame, self.degrees)

    def setDead(self):
        self.dead = 1
        self.game.Player.can_move = 1

    def onCollide(self, game):
        self.setDead()

    def update(self, index, ttime):
        for index, monster in enumerate(self.game.EntityHandler.monsters):
            if self.rect.colliderect(monster.rect):
                self.monster_index = index
                self.game.EntityHandler.monsters[index].takeDamage(index, self.damage)
                self.onCollide(self)
                return self.dead
        for solid in self.game.solid_list:
            if solid == 'LINK':
                pass
            elif self.rect.colliderect(solid):
                self.setDead()
        self.add()
        self.travelled += self.speed
        return self.dead

    def ranged_update(self, index, ttime):
        # used for ranged weapons, ex bows
        while self.collides_with_player:
            if self.rect.colliderect(self.game.Player.getRect()):
                self.add()
            else:
                self.sub(reps=5)
                self.collides_with_player = 0
        if self.travelled > self.range:
            self.setDead()
        self.add()
        self.travelled += self.speed
        return self.dead

    def fixed_update(self, index, ttime):
        # used for fixed position weapons, ex swords
        if self.retracting:
            if self.travelled <= 1:
                self.setDead()
            self.sub()
            self.travelled -= 1.5
        elif self.game.Player.collides(self.rect):
            self.game.Player.can_move = 0
            self.game.Player.player_state = 1
            self.add()
            self.travelled += 1
        else:
            self.retracting = 1
            self.sub()
        return self.dead

    def blit(self):
        self.game.screen.blit(self.frames[self.frame], self.game.off([self.pos[0], self.pos[1]]))