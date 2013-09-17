import pygame

from math import ceil
from os.path import join
'''
Class for managing invent(s)
Item storage format: Name:count:slotno;
'''

class Invent():
    def __init__(self, game):
        self.game = game
        self.shown = 0
        self.blit_items = []
        self.item_surfaces = []
        self.item_rects = []
        self.item_dummy_names = []
        self.in_hand = []
        self.slots = [[] for x in xrange(24)]
        self.inv_corner = [20, 0]
        self.inv_surf = pygame.image.load(join(game.main_path, 'rec', 'gui', 'inventory.png')).convert_alpha()
        self.inv_rect = self.inv_surf.get_rect()
        self.inv_rect.x = self.inv_corner[0]
        self.inv_rect.y = self.inv_corner[1]
        self.item_bg = pygame.image.load(join(game.main_path, 'rec', 'gui', 'item_bg.png')).convert_alpha()
        self.bg_rects = []
        self.reload()

    def reload(self):
        self.blit_items = []
        raw_cont = self.readInvent()
        if raw_cont:
            self.slots = self.parse(raw_cont)

        for index, slot in enumerate(self.slots):
            if self.shown:
                if slot:
                    self.blit_items.append(self.game.Item(self.game, slot[0], world=0))

    def add(self, item_name, slotno=-1):
        if self.hasItem(item_name):
            slot = self.getSlot(item_name)
            self.slots[slot][1] += 1
            self.sync()
        else:
            if slotno == -1:
                slotno = self.nextFreeSlot()
            self.slots[slotno] = [item_name, 1]
            self.sync()
        self.reload()
        if self.shown:
            self.loadInventSurfaces()

    def rem(self, slotindex):
        self.slots[slotindex] = []
        self.sync()

    def hasItem(self, name):
        for slot in self.slots:
            if slot:
                if slot[0] == name:
                    return True
        return False

    def getSlot(self, name):
        for index, slot in enumerate(self.slots):
            if slot:
                if slot[0] == name:
                    return index
        return False

    def nextFreeSlot(self):
        for index, slot in enumerate(self.slots):
            if not slot:
                return index
        return -1

    def sync(self):
        to_write = ''
        for index, slot in enumerate(self.slots):
            if slot:
                to_write += ('%s:%s:%s;') % (slot[0], slot[1], index)
        open(join(self.game.main_path, 'rec', 'user', 'invent.dat'), 'w').write(to_write)

    def readInvent(self):
        try:
            cont = open(join(self.game.main_path, 'rec', 'user', 'invent.dat'), 'r').read()
        except IOError:
            fi = open(join(self.game.main_path, 'rec', 'user', 'invent.dat'), 'w')
            fi.close()
            self.readInvent()
        else:
            return cont

    def parse(self, cont):
        slot_list = [[] for x in xrange(24)]
        items = cont.split(';')
        for item in items:
            if item:
                i = item.split(':')
                slot_list[int(i[2])] = [i[0], int(i[1])]
        return slot_list

    def draw(self):
        self.game.screen.blit(self.inv_surf, self.inv_corner)
        if self.shown:
            self.blitInvent()

    def getSurface(self, name):
        name = name.lower().replace(' ', '_') + '.png'
        return pygame.image.load(join(self.game.main_path, 'rec', 'items', name))


    def loadInventSurfaces(self):
        self.item_surfaces = []
        self.item_dummy_names = []
        self.item_rects = []
        for slot in self.slots:
            if slot:
                surf = self.getSurface(slot[0])
                self.item_surfaces.append(surf)
                self.item_rects.append(surf.get_rect())
                self.item_dummy_names.append(slot[0])

    def toggleView(self):
        if self.shown == 0:
            self.shown = 1
            self.loadInventSurfaces()
        else:
            self.shown = 0
            if self.in_hand:
                self.add(self.in_hand[0])
                self.in_hand = []

    def update(self):
        pass

    def inventClick(self, mouse):
        for index, rect in enumerate(self.item_rects):
            if rect.collidepoint(mouse):
                if self.in_hand:
                    self.add(self.in_hand[0])
                    self.in_hand = []
                clicked_name = self.item_dummy_names[index]
                self.in_hand = [clicked_name, self.item_surfaces[index], self.slots[self.getSlot(clicked_name)][1]]
                self.rem(self.getSlot(clicked_name))
                self.loadInventSurfaces()

    def testThrow(self, mpos):
        if not self.inv_rect.collidepoint(mpos):
            for _ in xrange(self.in_hand[2]):
                self.game.Item(self.game, self.in_hand[0], pos=self.game.Player.getPos(offset=[-1, -1]), spin=1, world=1)
            self.in_hand = []
        else:
            new_hand = []
            for index, rect in enumerate(self.bg_rects):
                if rect.collidepoint(mpos):
                    if self.slots[index]:
                        # item already in slot, add it to the hand and remove
                        new_hand = [self.slots[index][0], self.getSurface(self.slots[index][0]), self.slots[index][1]]
                        self.rem(index)
                    for _ in xrange(self.in_hand[2]):
                        self.add(self.in_hand[0], slotno=index)
                    self.in_hand = []
                    break
            if new_hand:
                self.in_hand = new_hand

    def blitInvent(self):
        #define formatting vars
        invent_dims = [224, 157]
        invent_corner = [182, 31]
        item_dim = 24
        padding = 10
        x = invent_corner[0] - item_dim + 5
        y = invent_corner[1] - item_dim + 5
        blit_count = 0
        items_blitted = 0
        self.bg_rects = []
        for index, slot in enumerate(self.slots):
            if not blit_count or blit_count == ceil(invent_dims[0] / (float(item_dim) + padding * 2.)):
                blit_count = 0
                y += item_dim + padding
                x = invent_corner[0] - item_dim + 5
            x += padding + item_dim
            self.bg_rects.append(self.game.screen.blit(self.item_bg, [x, y]))
            if slot:
                item_surf = self.item_surfaces[items_blitted]
                self.item_rects[items_blitted] = self.game.screen.blit(item_surf, [x, y])
                item_count = self.game.default_font.render(str(self.slots[index][1]), True, (255, 255, 255))
                self.game.screen.blit(item_count, [x + 19, y + 19])
                items_blitted += 1
            blit_count += 1
        if self.in_hand:
            mpos = list(pygame.mouse.get_pos())
            mpos[0] -= item_dim / 2
            mpos[1] -= item_dim / 2
            self.game.screen.blit(self.in_hand[1], mpos)