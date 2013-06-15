from globals import *
from math import ceil
'''
Class for managing invent
Item storage format: Name:[count];
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
        self.inv_corner = [20, 0]
        self.inv_surf = pygame.image.load(game.main_path + '\\rec\\gui\\inventory.png').convert_alpha()
        self.inv_rect = self.inv_surf.get_rect()
        self.inv_rect.x = self.inv_corner[0]
        self.inv_rect.y = self.inv_corner[1]
        self.item_bg = pygame.image.load(game.main_path + '\\rec\\gui\\item_bg.png').convert_alpha()
        self.reload()

    def reload(self):
        self.blit_items = []
        raw_cont = self.readInvent()
        if raw_cont:
            self.contents = self.parse(raw_cont)
        else:
            self.contents = {}

        for index, item in enumerate(self.contents):
            if not item:
                self.contents.pop(index)
            else:
                if self.shown:
                    self.blit_items.append(self.game.ItemHandler.load(item, world=0))

    def add(self, item):
        fi = open(self.game.main_path + '\\rec\\user\\invent.dat', 'a')
        inv_cont = self.readInvent()
        if ';%s:' % item['name'] in str(inv_cont):
            self.contents[item['name']] += 1
            self.sync()
        else:
            fi.write("%s:1;" % item['name'])
        fi.close()
        self.reload()
        if self.shown:
            self.item_surfaces = self.loadInventSurfaces()

    def rem(self, name):
        del self.contents[name]
        self.sync()

    def sync(self):
        to_write = ''
        for item in self.contents:
            if not self.contents[item]:
                del self.contents[item]
            to_write += ('%s:%s;') % (item, self.contents[item])
        open(self.game.main_path + '\\rec\\user\\invent.dat', 'w').write(to_write)

    def readInvent(self):
        try:
            cont = open(self.game.main_path + '\\rec\\user\\invent.dat', 'r').read()
        except IOError:
            fi = open(self.game.main_path + '\\rec\\user\\invent.dat', 'w')
            fi.close()
            self.readInvent()
        else:
            return cont

    def parse(self, cont):
        cont_dict = {}
        items = cont.split(';')
        for item in items:
            if item:
                i = item.split(':')
                cont_dict[i[0]] = int(i[1])
        return cont_dict

    def draw(self):
        self.game.screen.blit(self.inv_surf, self.inv_corner)
        if self.shown:
            self.blitInvent()

    def loadInventSurfaces(self):
        surf_list = []
        self.item_dummy_names = []
        self.item_rects = []
        for item in self.contents:
            surf = self.game.ItemHandler.getSurface(item)
            surf_list.append(surf)
            self.item_rects.append(surf.get_rect())
            self.item_dummy_names.append(item)
        return surf_list

    def toggleView(self):
        if self.shown == 0:
            self.shown = 1
            self.item_surfaces = self.loadInventSurfaces()
        else:
            self.shown = 0
            if self.in_hand:
                self.add(self.game.ItemHandler.load(self.in_hand[0], world=0))
                self.in_hand = []

    def update(self):
        pass

    def inventClick(self, mouse):
        for index, rect in enumerate(self.item_rects):
            if rect.collidepoint(mouse):
                if self.in_hand:
                    self.add(self.game.ItemHandler.load(self.in_hand[0], world=0))
                    self.in_hand = []
                clicked_name = self.item_dummy_names[index]
                self.in_hand = []
                self.in_hand.append(clicked_name)
                self.in_hand.append(self.item_surfaces[index])
                self.rem(clicked_name)
                self.item_surfaces = self.loadInventSurfaces()

    def testThrow(self, mpos):
        if not self.inv_rect.collidepoint(mpos):
            self.game.ItemHandler.load(self.in_hand[0], pos=self.game.Player.getPos(offset=[-25, -25]), spin=1, world=1)
            self.in_hand = []

    def blitInvent(self):
        #define formatting vars
        invent_dims = [224, 157]
        invent_corner = [182, 31]
        item_dim = 24
        padding = 10
        x = invent_corner[0] - item_dim + 5
        y = invent_corner[1] - item_dim + 5
        blit_count = 0
        for slot in xrange(24):
            blit_item = 1
            try:
                item = self.item_surfaces[slot]
            except IndexError:
                blit_item = 0
            if not blit_count or blit_count == ceil(invent_dims[0] / (float(item_dim) + padding * 2.)):
                blit_count = 0
                y += item_dim + padding
                x = invent_corner[0] - item_dim + 5
            x += padding + item_dim
            self.game.screen.blit(self.item_bg, [x, y])
            if blit_item:
                self.item_rects[slot] = self.game.screen.blit(item, [x, y])
            blit_count += 1
        if self.in_hand:
            mpos = list(pygame.mouse.get_pos())
            mpos[0] -= item_dim / 2
            mpos[1] -= item_dim / 2
            self.game.screen.blit(self.in_hand[1], mpos)