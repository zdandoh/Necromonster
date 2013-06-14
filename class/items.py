from uuid import uuid4
from random import randrange
from pygame.image import load

class Item():
    def __init__(self, game):
        self.world_items = []
        self.game = game

    def load(self, name, pos=[0, 0], spin=0, world=1):
        item = {}
        item['name'] = name
        item['file'] = name.lower().replace(' ', '_') + '.png'
        item['pos'] = pos
        item['id'] = uuid4()
        item['image'] = load(self.game.main_path + '\\rec\\items\\' + item['file'])
        item['rect'] = item['image'].get_rect()
        item['rect'].x = item['pos'][0]
        item['rect'].y = item['pos'][1]
        if spin:
            item['vector'] = [randrange(0, 3), randrange(0, 3)]
        else:
            item['vector'] = [0, 0]
        # decides to put item in world or not
        if world:
            self.world_items.append(item)
        return item

    def getSurface(self, name):
        name = name.lower().replace(' ', '_') + '.png'
        return load(self.game.main_path + '\\rec\\items\\' + name)

    def update(self):
        for index, item in enumerate(self.world_items):
            if self.game.Player.collides(item['rect']):
                rem_item = self.world_items.pop(index)
                self.game.Invent.add(rem_item)
                self.game.Player.headDraw(item['name'])

    def blitItems(self):
        all_items = []
        for item in self.world_items:
            all_items.append([item['image'], item['pos']])
        return all_items

    def clear(self):
        self.world_items = []