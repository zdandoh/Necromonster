from pygame.image import load
from pygame.transform import rotate

class Projectile():
    def __init__(self, game, damage, degrees, pos, vector, speed, range, surf_path, type='dagger'):
        # general vars
        self.game = game
        self.degrees = degrees
        self.type = type
        self.speed = speed
        self.vector = vector
        self.surf = load(surf_path)
        self.turn()
        self.dims = list(self.surf.get_size())
        self.rect = self.surf.get_bounding_rect()
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
        
        self.game.EntityHandler.projectiles.append(self)

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

    def turn(self):
        if self.type == 'dagger':
            if 135 > self.degrees >= 45:
                self.surf = rotate(self.surf, 90)
                self.vector = [-self.speed, 0] # left
            elif 225 > self.degrees >= 135:
                self.surf = rotate(self.surf, 180)
                self.vector = [0, self.speed] # back
            elif 315 > self.degrees >= 225:
                self.surf = rotate(self.surf, 270)
                self.vector = [self.speed, 0] # right
            else:
                self.surf = rotate(self.surf, 0)
                self.vector = [0, -self.speed] # up
        elif self.type == 'ranged':
            self.surf = rotate(self.surf, self.degrees)
        else:
            raise TypeError("Can't turn {}".format(self.type))

    def setDead(self):
        self.dead = 1
        self.game.Player.can_move = 1

    def update(self, index, ttime):
        if self.type == 'ranged':
            self.dead = self.ranged_update(index, ttime)
        elif self.type == 'fixed':
            self.dead = self.fixed_update(index, ttime)
        for index, monster in enumerate(self.game.EntityHandler.monsters):
            if self.rect.colliderect(monster.rect):
                self.game.EntityHandler.monsters[index].takeDamage(index, self.damage)
                self.setDead()
                return self.dead
        for solid in self.game.solid_list:
            if solid == 'LINK':
                pass
            elif self.rect.colliderect(solid):
                self.setDead()
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
        self.game.screen.blit(self.surf, self.game.off([self.pos[0], self.pos[1]]))