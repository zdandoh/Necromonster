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
        self.inv_surf = pygame.image.load(game.main_path + '\\rec\\gui\\inventory.png').convert_alpha()
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

    def sync(self):
        to_write = ''
        for item in self.contents:
            to_write += ('%s:%s;') % (item, self.contents[item])
        open(self.game.main_path + '\\rec\\user\\invent.dat', 'w').write(to_write)
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
        self.game.screen.blit(self.inv_surf, [20, 0])
        if self.shown:
            self.blitInvent()

    def loadInventSurfaces(self):
        surf_list = []
        for item in self.contents:
            surf_list.append(self.game.ItemHandler.getSurface(item))
        return surf_list

    def toggleView(self):
        if self.shown == 0:
            self.shown = 1
            self.item_surfaces = self.loadInventSurfaces()
        else:
            self.shown = 0

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
                self.game.screen.blit(item, [x, y])
            blit_count += 1