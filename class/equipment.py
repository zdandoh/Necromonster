import os

from pygame.image import load as img_load
from pygame import Surface
from pygame import Rect
from pygame.transform import rotate
from pygame.draw import circle
from items import Item


class Weapon(Item):
    def __init__(self, game, name):
        """
        Slightly depreciated weapon class. Will need major rewriting.
        Used for loading and applying weapon characteristics to the player.
        """
        self.game = game
        #setup base vars of all weapon(s)
        self.type = None
        self.shown = True
        self.range = 10
        self.damage = 1
        self.cooldown = 500 # in MS
        self.speed = 4
        self.projectile = None
        self.loadWeapon(name)

        # attack based vars
        self.attacking = False

    def loadWeapon(self, name):
        """
        Uses the weapon config file to load all weapon characteristics.
        """
        config_file = open(os.path.join('rec', 'weapon', name, 'config.py')).read()
        exec(config_file)
        self.hold_image = img_load(os.path.join('rec', 'weapon', name, 'hold.png')).convert_alpha()
        if os.path.exists(os.path.join('rec', 'weapon', name, 'attack.png')):
            self.attack_image = img_load(os.path.join('rec', 'weapon', name, 'attack.png')).convert_alpha()
        else:
            self.attack_image = Surface([1, 1])

    def getSurface(self, name):
        fi_name = name.lower().replace(' ', '_') + '.png'
        return img_load(os.path.join(self.game.main_path, 'rec', 'weapon', name, fi_name))

    def preUpdate(self, ttime):
        """
        Called before the update function, can be overriden for new functionality.
        """
        pass

    def update(self, ttime):
        """
        Main weapon update, should not be overriden.
        """
        self.preUpdate(ttime)
        if self.type == 'short':
            self.shortUpdate()
        elif self.type == 'long':
            self.longUpdate()
        elif self.type == 'ranged':
            self.rangedUpdate()
        else:
            pass

    def shortAttack(self):
        self.attacking = True
        if self.game.Player.player_face == 'front':
            # I do not know why this vector needs to be 0 while the others are like, 1
            self.directional_attack_image = rotate(self.attack_image, 180)
            self.sub_vector = [0, 0]
        elif self.game.Player.player_face == 'left':
            self.directional_attack_image = rotate(self.attack_image, 90)
            self.sub_vector = [-1, 0]
        elif self.game.Player.player_face == 'back':
            self.directional_attack_image = rotate(self.attack_image, 0)
            self.sub_vector = [0, -1]
        elif self.game.Player.player_face == 'right':
            self.directional_attack_image = rotate(self.attack_image, 270)
            self.sub_vector = [0.8, 0] # editing this seems to change the speed of the right dagger swing a bit

        self.game.Player.can_move = False
        self.receding = False
        self.potent = True
        self.weapon_rect = Rect(1, 1, 1, 1)
        p_coords = [self.game.Player.player_r.x, self.game.Player.player_r.y]
        a_coords = [p_coords[0] + self.game.Player.getRigging()[0], p_coords[1] + self.game.Player.getRigging()[1]]
        if self.game.Player.player_face == 'right' or self.game.Player.player_face == 'left':
            a_coords = [a_coords[0] - self.attack_image.get_height(), a_coords[1] - self.attack_image.get_width()]
        self.blit_pos = a_coords
        self.attack_ticks = self.range


    def shortUpdate(self):
        if self.attacking:
            for repeats in xrange(self.speed):
                self.game.Player.player_state = 3
                self.blit_pos[0] += self.sub_vector[0]
                self.blit_pos[1] += self.sub_vector[1]
                if self.receding:
                    self.attack_ticks += 1
                elif not self.receding:
                    self.attack_ticks -= 1
                # check all monsters for touching weapon
                for index, monster in enumerate(self.game.EntityHandler.monsters):
                    if monster.rect.colliderect(self.weapon_rect):
                        if self.potent:
                            monster.takeDamage(index, self.damage)
                            self.potent = False

        if self.attacking and self.attack_ticks == self.range and self.receding:
            self.attacking = False
            self.game.Player.can_move = True
        elif self.attacking and self.attack_ticks <= 0 and not self.receding:
            self.receding = True
            self.sub_vector[0] *= -1
            self.sub_vector[1] *= -1

    def shortBlit(self):
        if self.attacking:
            if self.game.Player.player_face == 'front' or self.game.Player.player_face == 'back':
                height = self.directional_attack_image.get_rect().height
                d_rect = Rect([0, height - (self.range - self.attack_ticks)], [100, 100])
                self.weapon_rect = self.game.screen.blit(self.directional_attack_image, self.game.off([self.blit_pos[0], self.blit_pos[1]]), d_rect)
                unoff_pos = self.game.unoff([self.weapon_rect.x, self.weapon_rect.y])
                self.weapon_rect.x = unoff_pos[0]
                self.weapon_rect.y = unoff_pos[1]
            elif self.game.Player.player_face == 'right' or self.game.Player.player_face == 'left':
                pos = self.game.off([self.blit_pos[0] + self.rigging[1], self.blit_pos[1]])
                if self.game.Player.player_face == 'left':
                    #this prevents the "hover" look of the dagger off the default player body
                    pos[0] += 7
                width = self.directional_attack_image.get_rect().width
                d_rect = Rect([width - (self.range - self.attack_ticks), 0], [100, 100])
                self.weapon_rect = self.game.screen.blit(self.directional_attack_image, pos, d_rect)
                unoff_pos = self.game.unoff([self.weapon_rect.x, self.weapon_rect.y])
                self.weapon_rect.x = unoff_pos[0]
                self.weapon_rect.y = unoff_pos[1]

    def longAttack(self):
        self.attacking = True
        if self.game.Player.player_face == "front":
            self.init_angle = 180
            self.directional_attack_image = rotate(self.attack_image, self.init_angle)
        self.angle = 0

    def longUpdate(self):
        if self.attacking:
            for x in xrange(5):
                self.mod_DAT = self.game.rotopoint(self.directional_attack_image, self.angle+45, [3, 0])
                if self.angle < -50:
                    self.attacking = False
                self.angle -= 1

    def longBlit(self):
        if self.attacking:
            blit_pos = self.game.off(self.game.Player.getPos())
            self.game.screen.blit(self.mod_DAT, blit_pos)

    def rangedAttack(self):
        pass

    def rangedUpdate(self):
        pass

    def rangedBlit(self):
        pass

    def blit(self):
        """
        Called before the player is blitted
        """
        if self.game.Player.player_face == 'back' and not self.attacking:
            self.drawInHand()
        if self.type == 'short':
            self.shortBlit()
        elif self.type == 'long':
            self.longBlit()
        elif self.type == 'ranged':
            self.rangedBlit()

    def blitAfter(self):
        if self.game.Player.player_face == 'front' and not self.attacking:
            self.drawInHand()

    def drawInHand(self):
        p_coords = [self.game.Player.player_r.x, self.game.Player.player_r.y]
        a_coords = [p_coords[0] + self.game.Player.getRigging()[0] - self.game.Player.equipment['weapon'].rigging[0], p_coords[1] + self.game.Player.getRigging()[1] - self.game.Player.equipment['weapon'].rigging[1]]
        self.game.screen.blit(self.hold_image, self.game.off(a_coords))

    def onClick(self, game, vector):
        """
        Called when the world is clicked. Activates the weapon.
        """
        if self.projectile:
            game.Projectile(game, self.projectile, vector)
        if self.type == 'short':
            self.shortAttack()
        elif self.type == 'long':
            self.longAttack()
        elif self.type == 'ranged':
            self.rangedAttack()


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
        self.game.Player.stats['defense'] += self.defense

    def remove(self):
        """
        Called when the garment is removed.
        Must be properly modified along with apply() if additional effects need to be removed.
        """
        self.game.Player.stats['defense'] -= self.defense