import pygame
from pygame.locals import *

import mapLoader
from Entity import Entity

import math
import os
import time
from ast import literal_eval


class Player(Entity):
    def __init__(self, game):
        """
        Main player class. Controls all player movement, updates, and state data.
        """
        self.player = pygame.image.load(os.path.join('rec', 'entity', 'player', 'img', 'back1.png'))
        super(Player, self).__init__(game, self.player)
        self.head_font = pygame.font.Font(os.path.join('rec', 'font', 'p_head.ttf'), 15)
        self.can_move = 1
        self.knocked = 0
        self.takeover_finished = 1
        self.player_face = 'back'  # this is the part of the player that you see
        self.player_state = 1.
        self.head_drawn = 0
        self.player_masks = {}
        self.player_r = self.player.get_rect()
        self.player_dims = self.player.get_size()
        # get initial player riggings
        self.riggings = {}
        execfile(os.path.join('rec', 'entity', 'player', 'config.py'))

        # setup attack vars
        self.last_attack = pygame.time.get_ticks()

        self.player_frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'entity', 'player', 'img')):
            if fi.endswith('.png'):
                self.player_frames[fi] = pygame.image.load(os.path.join(self.game.main_path, 'rec', 'entity', 'player', 'img', fi)).convert_alpha()
        self.getMasks(self.player_frames.keys(), self.player_frames.values())

        self.player_r.x = 450
        self.player_r.y = 650

        # stats
        self.stats = {}
        self.stats['hp'] = 10
        self.stats['maxhp'] = 10
        self.stats['maxpxp'] = 1000
        self.stats['maxmxp'] = 1000
        self.stats['pxp'] = 312
        self.stats['mxp'] = 654
        self.stats['attack'] = 1
        self.stats['defense'] = 0

        # equipment
        self.game.Player = self
        self.equipment = {}
        self.equipment['head'] = self.game.Garment(self.game, 'nothing')
        self.equipment['chest'] = self.game.Garment(self.game, 'nothing')
        self.equipment['legs'] = self.game.Garment(self.game, 'nothing')
        self.equipment['a1'] = self.game.Garment(self.game, 'nothing')
        self.equipment['a2'] = self.game.Garment(self.game, 'nothing')
        self.equipment['weapon'] = self.game.Weapon(self.game, 'nothing')
        self.loadEquip(25)
        self.loadEquip(26)
        self.loadEquip(27)
        self.loadEquip(28)
        self.loadEquip(29)
        self.loadEquip(30)

    def update(self, ttime):
        """
        Update player position based on keypresses. Tests for collision against buildings.
        Updates frames as the player walks.
        """
        self.preUpdate()
        if 1 in self.game.keys_pressed and self.can_move:
            if self.game.keys_pressed[K_w]:
                self.player_r.y += -2
                self.onMove([0, -2])
                self.player_face = 'back'
            if self.game.keys_pressed[K_a]:
                self.player_r.x += -2
                self.onMove([-2, 0])
                self.player_face = 'left'
            if self.game.keys_pressed[K_s]:
                self.player_r.y += 2
                self.onMove([0, 2])
                self.player_face = 'front'
            if self.game.keys_pressed[K_d]:
                self.player_r.x += 2
                self.onMove([2, 0])
                self.player_face = 'right'

            self.player_state += 0.15
            if self.player_state >= 4.:
                self.player_state = 1.
        if not self.game.keys_pressed[K_w] and not self.game.keys_pressed[K_a] and not self.game.keys_pressed[K_s] and not self.game.keys_pressed[K_d] and self.can_move:
            self.player_state = 1.
        self.player = self.player_frames['%s%s.png' % (self.player_face, int(self.player_state))]

        self.equipment['weapon'].update(ttime)
        if self.equipment['weapon'].shown == 1:
            self.equipment['weapon'].blit()

    def preUpdate(self):
        """
        An overwritable function to add temp player functionality
        """
        pass

    def loadEquip(self, slot):
        """
        Checks a slot for equipment and adds its effects to the player.
        """
        type = self.game.Garment
        if slot == 25:
            slice = 'weapon'
            type = self.game.Weapon
        elif slot == 26:
            slice = 'head'
        elif slot == 27:
            slice = 'chest'
        elif slot == 28:
            slice = 'legs'
        elif slot == 29:
            slice = 'a1'
        elif slot == 30:
            slice = 'a2'
        else:
            #not an equipment slot
            #raise ValueError('Slot # {} is not a valid equipment slot'.format(slot))
            return -1
        if self.game.Invent.slots[slot]:
            name = self.game.Invent.slots[slot][0]
            self.equipment[slice] = type(self.game, name)
        else:
            self.removeGarment(slice)
            self.equipment[slice] = type(self.game, 'nothing')

    def removeGarment(self, name):
        """
        Called when a Garment object is remove from the player.
        """
        if name == 'weapon':
            return 0
        self.stats['defense'] -= self.equipment[name].getDefense()

    def setRigging(self, front, back, left, right):
        """
        Set the rigging for each part of the player.
        """
        self.riggings['front'] = front
        self.riggings['back'] = back
        self.riggings['left'] = left
        self.riggings['right'] = right

    def getRigging(self):
        return self.riggings[self.player_face]

    def isVertical(self):
        if self.game.Player.player_face == "back" or self.game.Player.player_face == "front":
            return True
        else:
            return False

    def isHorizontal(self):
        if self.game.Player.player_face == "left" or self.game.Player.player_face == "right":
            return True
        else:
            return False


    def onMove(self, offset, link_count = 0):
        """
        Called when the player moves. Used to make sure new positions are valid.
        Returns player to old location if not valid.
        """
        m_rects = [x.rect for x in self.game.EntityHandler.monsters]
        if self.player_r.x > self.game.Grid.bounds[0] or self.player_r.x <= 0:
            self.player_r.x -= offset[0]
        if self.player_r.y > self.game.Grid.bounds[1] or self.player_r.y <= 0:
            self.player_r.y -= offset[1]
        for rect in self.game.solid_list + m_rects:
            link_active = 0
            if 'LINK' in rect:
                link = self.game.links[link_count]
                rect = literal_eval(link[1])
                link_count += 1
                link_active = 1
            if self.player_r.colliderect(rect):
                if link_active:
                    if self.game.keys_pressed[K_SPACE]:
                        self.game.blit_list = mapLoader.load(link[2], self.game, new_pos = link[3], face = link[4])
                else:
                    #bring on mask collision
                    mask = pygame.mask.Mask((rect.width, rect.height))
                    mask.fill()
                    player_mask = self.player_masks[self.player_face + str(int(self.player_state)) + '.png']
                    offset_x = self.player_r.x - rect.x
                    offset_y = self.player_r.y - rect.y

                    if mask.overlap(player_mask, (offset_x, offset_y)):
                        self.player_r.y -= offset[1]
                        self.player_r.x -= offset[0]

    def getDegrees(self):
        """
        If the screen is a circle and the player is at the center, 
        this function is used to get the degree that the mouse pointer lies on.
        """
        ppos = self.game.center_point
        mpos = pygame.mouse.get_pos()

        angle = math.degrees(math.atan2(ppos[0]-mpos[0], ppos[1]-mpos[1]))
        if angle < 0:
            angle += 360

        return angle

    def takeOver(self, monster):
        """
        Called when the player attempts to take over a monster.
        Applies all new equipment, attributes, and inventory.
        """
        if monster.NPC:
            return False
        if self.takeover_finished:
            self.takeover_finished = 0
            #replace all player stats and frames with monster
            self.stats['hp'] = int(monster.hp)
            self.stats['maxhp'] = int(monster.maxhp)
            self.stats['attack'] = int(monster.attack)
            self.stats['defense'] = int(monster.defense)
            self.stats['speed'] = int(monster.speed)
            self.riggings = monster.riggings
            mframe = monster.frames[monster.frames.keys()[0]]
            px = self.player_r.x
            py = self.player_r.y
            self.player_r = mframe.get_rect()
            self.player_dims = mframe.get_size()
            self.player_r.x = px
            self.player_r.y = py

            def preUpdate():
                self.can_move = 0
                if time.time() - self.takeover_time > 0.20 - self.takeover_cycles:
                    if self.takeover_cycles > 0.20:
                        #finish the cycle
                        self.preUpdate = self.old_preUpdate
                        self.can_move = 1
                        self.takeover_finished = 1
                        self.game.EntityHandler.monsters[self.takeover.index].dead = 1
                        self.weapon = self.game.Weapon(self.game, self.game.EntityHandler.monsters[self.takeover.index].weapon)
                    self.takeover_cycles += 0.01
                    if self.frame_type == 0:
                        self.game.EntityHandler.monsters[self.takeover.index].frames = self.takeover_pframes
                        self.player_frames = self.takeover_mframes
                        self.frame_type = 1
                    elif self.frame_type == 1:
                        self.game.EntityHandler.monsters[self.takeover.index].frames = self.takeover_mframes
                        self.player_frames = self.takeover_pframes
                        self.frame_type = 0
                    else:
                        raise ValueError('Frame type of {} is invalid'.format(self.frame_type))
                    self.takeover_time = time.time()

            self.player = monster.frames['front1.png']
            self.getMasks(monster.frames.keys(), monster.frames.values())
            self.can_move = 0
            self.game.EntityHandler.monsters[monster.index].can_move = 0

            #setup all the vars used in the preupdate function
            self.takeover = monster
            self.takeover_time = time.time()
            self.takeover_cycles = 0
            self.frame_type = 0
            self.game.Invent = self.game.Inventory(self.game, fi=monster.name + '.dat')
            self.takeover_pframes = self.player_frames
            self.takeover_mframes = monster.frames
            self.old_preUpdate = self.preUpdate
            self.preUpdate = preUpdate

    def getMasks(self, names, frames):
        """
        Get the pixel masks of all player/monster frames.
        """
        self.player_masks = {}
        for name, frame in zip(names, frames):
            self.player_masks[name] = pygame.mask.from_surface(frame)

    def headDraw(self, text, rect, dur=3, off=True):
        """
        Draw the text at the head of the player rect. Default duration of 3 seconds.
        """
        text = text.replace('_', ' ')
        font_render = self.head_font.render(text, True, (255, 255, 255))
        render_pos = [rect.x - font_render.get_size()[0] / 2 + rect.w / 2, rect.y - 25]
        if off:
            render_pos = self.game.off(render_pos)
        self.head_drawn = [font_render, render_pos, pygame.time.get_ticks() + dur, off]
        self.game.Scheduler.add('self.game.Player.head_drawn = ""', dur * 1000)

    def addPos(self, move):
        self.player_r.x += move[0]
        self.player_r.y += move[1]

    def move(self, change):
        self.addPos(change)
        self.onMove(change)

    def collides(self, rect):
        """
        Mostly unused function to save typing. ?(Depreciated)?
        """
        return self.player_r.colliderect(rect)

    def setPos(self, new):
        self.player_r.x = new[0]
        self.player_r.y = new[1]

    def getRect(self):
        return Rect(self.player_r)

    def getPos(self, offset=[0, 0]):
        return [self.player_r.x + offset[0], self.player_r.y + offset[1]]

    def getNode(self):
        return (self.player_r.x + 20) / 10, (self.player_r.y + 30) / 10

    def getDistance(self, rect):
        """
        Gets the distance that the player is from a certain rect.
        """
        return math.hypot(self.player_r.x - rect.x, self.player_r.y - rect.y)

    def setFace(self, face, state=1):
        """
        Set the face of the player that is shown.
        """
        face = face.replace('\r', '')
        if face:
            self.player_face = face

    def attack(self, mpos):
        """
        Called when the player attacks. Currently unused with few weapon types added.
        """
        # (y - y) / (x - x)
        degrees = self.getDegrees()
        if 135 > degrees >= 45:
            self.setFace('left')
        elif 225 > degrees >= 135:
            self.setFace('front')
        elif 315 > degrees >= 225:
            self.setFace('right')
        else:
            self.setFace('back')
        speed = 4.
        range = 200
        distance = [mpos[0] - self.game.center_point[0], mpos[1] - self.game.center_point[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]

        self.equipment['weapon'].onClick(self.game, bullet_vector)

    def takeDamage(self, damage):
        """
        Called when the player takes damage.
        """
        damage -= self.stats['defense']
        if self.stats['hp'] > 0:
            if damage <= 0:
                damage = 1
            self.stats['hp'] -= damage

    def blitPlayer(self):
        """
        Draws the player on the screen object.
        """
        self.equipment['weapon'].blit()
        self.game.screen.blit(self.player, self.game.off([self.player_r.x, self.player_r.y]))
        self.equipment['weapon'].blitAfter()