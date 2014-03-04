import os

from pygame.image import load as img_load
from items import Item


class Weapon(Item):
    def __init__(self, game, name):
        """
        Slightly depreciated weapon class. Will need major rewriting.
        Used for loading and applying weapon characteristics to the player.
        """
        self.game = game
        super(Weapon, self).__init__(game, name, world=0)
        #setup base vars of all weapon(s)
        self.type = None
        self.shown = 0
        self.projectile = False
        self.range = 50
        self.dead = 0
        self.frame = 0
        self.loadWeapon(name)

    def changeUpdate(self):
        """
        Overrides an update type based on weapon type attribute.
        """
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

    def loadWeapon(self, name):
        """
        Uses the weapon config file to load all weapon characteristics.
        """
        config_file = open(os.path.join('rec', 'weapon', name, 'config.py')).read()
        exec(config_file)
        self.frames = []
        for fi in os.listdir(os.path.join('rec', 'weapon', name)):
            if '.png' in fi:
                self.frames.append(img_load(os.path.join('rec', 'weapon', name, fi)))
        self.changeUpdate()

    def getSurface(self, name):
        fi_name = name.lower().replace(' ', '_') + '.png'
        return img_load(os.path.join(self.game.main_path, 'rec', 'weapon', name, fi_name))

    def preUpdate(self, index, ttime):
        """
        Called before the update function, can be overriden for new functionality.
        """
        self.update(index, ttime)

    def updateWeapon(self, index, ttime):
        """
        Dummy method for updating a weapon. Always overriden.
        """
        pass

    def blit(self):
        """
        Displays the weapon on screen. Really broken, I believe.
        """
        if self.shown:
            self.game.screen.blit(self.frames[self.frame], self.game.off([self.game.Player.player_r.x, self.game.Player.player_r.y]))
        else:
            self.game.screen.blit(self.frames[self.frame], self.game.off(self.pos))

    def onClick(self, game, vector):
        """
        Called when the world is clicked. Activates the weapon.
        """
        if self.projectile:
            game.Projectile(game, self.projectile, vector)

    def create(self):
        """
        Creates the weapon object and adds it to the EntityHandler.
        """
        self.pos = [self.game.Player.player_r.x, self.game.Player.player_r.y]
        self.game.EntityHandler.misc.append(self)


class Garment(Item):
    def __init__(self, game, name):
        """
        Class for armor and accessories. New armor must be registered here when added.
        """
        super(Garment, self).__init__(game, name, world=0)
        # the following few lines of code are a waste of memory. Too bad I don't have the STATIC keyword.
        self.head = {'leather_hat': 1}
        self.chest = {'leather_shirt': 2}
        self.pants = {'leather_pants': 1}
        self.all_garments = dict(self.head.items() + self.chest.items() + self.pants.items())
        self.name = name
        self.type = None
        self.defense = self.getDefense()
        self.apply()

    def getDefense(self):
        """
        Returns an int. The defense of a Garment.
        """
        #returns defense of Garment based on name
        defense = 0
        try:
            defense = self.all_garments[self.name]
        except KeyError:
            # no garment of that name
            self.belongs = False
        return defense

    def apply(self):
        """
        Used to apply the effects of a garment to the player.
        Can be overriden for additional effects.
        """
        # add effects to the player
        self.game.Player.stats['defense'] += self.defense

    def remove(self):
        """
        Called when the garment is removed.
        Must be properly modified along with apply() if additional effects need to be removed.
        """
        #called when player takes off garment
        self.game.Player.stats['defense'] -= self.defense


def daggerUpdate(index, ttime):
    pass

def swordUpdate(index, ttime):
    pass

def rangedUpdate(index, ttime):
    pass

def staffUpdate(index, ttime):
    pass