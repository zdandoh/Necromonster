from uuid import uuid4
from random import randrange
from pygame.image import load

class Item():
    def __init__(self, game):
        self.items = []
        self.game = game

    def add(self, name, pos=[0, 0], spin=[0, 0], type='png'):
        item = {}
        item['name'] = name
        item['file'] = name.lower().replace(' ', '_') + '.%s' % type
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
        self.items.append(item)

    def update(self):
        for index, item in enumerate(self.items):
            if self.game.Player.collides(item['rect']):
                rem_item = self.items.pop(index)
                self.game.Invent.add(rem_item)
                self.game.Player.headDraw(item['name'])

    def blitItems(self):
        all_items = []
        for item in self.items:
            all_items.append([item['image'], item['pos']])
        return all_items

    def clear(self):
        self.items = []