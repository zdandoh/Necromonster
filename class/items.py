from uuid import uuid4
from pygame.image import load
from os.path import join

class Item():
    def __init__(self, game, name, pos=[0, 0], spin=0, world=1):
        self.game = game
        self.name = name
        self.file = name.lower().replace(' ', '_') + '.png'
        self.pos = pos
        self.dead = 0
        self.id = uuid4()
        self.image = load(join(self.game.main_path, 'rec', 'items', self.file))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        if spin:
            self.vector = [-7, -7]
        else:
            self.vector = [0, 0]
        # decides to put item in world or not
        if world:
            self.game.EntityHandler.world_items.append(self)

    def getSurface(self, name):
        name = name.lower().replace(' ', '_') + '.png'
        return load(join(self.game.main_path, 'rec', 'items', name))

    def update(self, index, ttime):
        if self.dead:
            return 1
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]
        if sum(self.vector):
            if self.vector[0] < 0:
                self.vector[0] += 1
            elif self.vector[0] > 0:
                self.vector[0] -= 1
            if self.vector[1] < 0:
                self.vector[1] += 1
            elif self.vector[1] > 0:
                self.vector[1] -= 1
        if self.game.Player.collides(self.rect) and not sum(self.vector):
            self.game.Invent.add(self.name)
            self.game.Player.headDraw(self.name)
            self.dead = 1

    def blit(self):
        self.game.screen.blit(self.image, self.game.off(self.pos))

    def clear(self):
        '''Used for moving to new maps'''
        self.world_items = []