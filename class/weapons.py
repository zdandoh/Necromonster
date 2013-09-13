import os

from pygame.image import load as img_load

class Weapon():
    def __init__(self, name, game):
        self.game = game
        #setup base vars of all weapons
        self.type = None
        self.shown = 0
        self.projectile = False
        self.range = 50
        self.dead = 0
        self.frame = 0
        self.load(name)

    def changeUpdate(self):
        if not self.type:
            raise ValueError('No weapon type specified')
        elif self.type == 'dagger':
            self.update = daggerUpdate
        elif self.type == 'sword':
            self.update = swordUpdate
        elif self.type == 'ranged':
            self.update = rangedUpdate
        elif self.type == 'staff':
            self.update = staffUpdate
        else:
            raise ValueError('No weapon of type {}'.format(self.type))

    def load(self, name):
        config_file = open(os.path.join('rec', 'weapon', name, 'config.py')).read()
        exec(config_file)
        self.frames = []
        for fi in os.listdir(os.path.join('rec', 'weapon', name)):
            if '.png' in fi:
                self.frames.append(img_load(os.path.join('rec', 'weapon', name, fi)))
        self.changeUpdate()

    def preUpdate(self, index, ttime):
        self.update(index, ttime)

    def update(self, index, ttime):
        pass

    def blit(self):
        if self.shown:
            self.game.screen.blit(self.frames[self.frame], self.game.off([self.game.Player.player_r.x, self.game.Player.player_r.y]))
        else:
            self.game.screen.blit(self.frames[self.frame], self.game.off(self.pos))

    def onClick(self, game, vector):
        game.Projectile(game, self.projectile, vector)

    def create(self):
        self.pos = [self.game.Player.player_r.x, self.game.Player.player_r.y]
        self.game.EntityHandler.misc.append(self)


def daggerUpdate(index, ttime):
    pass

def swordUpdate(index, ttime):
    pass

def rangedUpdate(index, ttime):
    pass

def staffUpdate(index, ttime):
    pass