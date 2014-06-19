

class Entity(object):
    def __init__(self, game, surface):
        self.game = game
        self.surface = surface
        self.size = self.getSize()
        self.rect = self.surface.get_rect()

    def getPos(self):
        return [self.rect.x, self.rect.y]

    def setPos(self, newpos):
        self.rect.x = newpos[0]
        self.rect.y = newpos[1]

    def getSize(self):
        self.size = self.surface.get_size()
        return self.size

    def collide(self, other_rect):
        return self.rect.colliderect(other_rect)

    def update(self):
        pass

    def draw(self):
        self.game.screen.blit(self.surface, self.getPos())