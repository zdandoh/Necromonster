from pygame.image import load
from pygame.transform import rotate

class Projectile():
    def __init__(self, game, damage, degrees, pos, vector, speed, range, surf_path):
        self.game = game
        self.surf = load(surf_path)
        self.surf = rotate(self.surf, degrees)
        self.rect = self.surf.get_rect()
        self.vector = vector
        self.speed = speed
        self.range = range
        self.damage = damage
        self.dead = 0
        self.travelled = 0
        self.collides_with_player = 1
        self.pos = [float(pos[0]), float(pos[1])]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def add(self):
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def sub(self, reps=1):
        for _ in xrange(reps):
            self.pos[0] -= self.vector[0]
            self.pos[1] -= self.vector[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def update(self):
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
        for index, monster in enumerate(self.game.Monster.monsters):
            if self.rect.colliderect(monster['rect']):
                self.game.Monster.attack(index, self.damage)
                self.dead = 1
                return self.dead
        for solid in self.game.solid_list:
            if solid == 'LINK':
                pass
            elif self.rect.colliderect(solid):
                self.dead = 1
        return self.dead

    def blit(self):
        self.game.screen.blit(self.surf, self.game.off([self.pos[0], self.pos[1]]))