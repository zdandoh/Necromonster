from pygame.image import load
from pygame.transform import rotate

class Projectile():
    def __init__(self, game, damage, degrees, pos, vector, speed, range, surf_path, type='fixed'):
        self.game = game
        self.surf = load(surf_path)
        self.surf = rotate(self.surf, degrees)
        self.dims = list(self.surf.get_size())
        self.rect = self.surf.get_rect()
        self.vector = vector
        self.speed = speed
        self.range = range
        self.damage = damage
        self.dead = 0
        self.travelled = 0
        self.type = type
        self.collides_with_player = 1
        self.pos = [float(pos[0]) - (self.surf.get_size()[0] / 2), float(pos[1]) - (self.surf.get_size()[1])]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.game.EntityHandler.projectiles.append(self)

    def add(self):
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def sub(self, reps=1):
        print reps
        for _ in xrange(reps):
            self.pos[0] -= self.vector[0]
            self.pos[1] -= self.vector[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def update(self, index, ttime):
        if self.type == 'ranged':
            self.dead = self.ranged_update(index, ttime)
        elif self.type == 'fixed':
            self.dead = self.fixed_update(index, ttime)
        for index, monster in enumerate(self.game.EntityHandler.monsters):
            if self.rect.colliderect(monster.rect):
                self.game.EntityHandler.monsters[index].takeDamage(index, self.damage)
                self.dead = 1
                return self.dead
        for solid in self.game.solid_list:
            if solid == 'LINK':
                pass
            elif self.rect.colliderect(solid):
                self.dead = 1
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
            self.dead = 1
        self.add()
        self.travelled += self.speed
        return self.dead

    def fixed_update(self, index, ttime):
        # used for fixed position weapons, ex swords
        self.add()
        return self.dead

    def blit(self):
        self.game.screen.blit(self.surf, self.game.off([self.pos[0], self.pos[1]]))