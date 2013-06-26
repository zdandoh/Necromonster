from pygame.image import load
from pygame.transform import rotate

class Projectile():
    def __init__(self, game, damage, degrees, pos, vector, surf_path):
        self.game = game
        self.surf = load(surf_path)
        self.surf = rotate(self.surf, degrees)
        self.rect = self.surf.get_bounding_rect()
        self.vector = vector
        self.damage = damage
        self.dead = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]
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
        self.game.screen.blit(self.surf, self.game.off([self.rect.x, self.rect.y]))