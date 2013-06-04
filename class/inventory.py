from globals import *

class Invent():
    def __init__(self, game):
        self.game = game
        self.reload()

    def reload(self):
        try:
            self.contents = open(self.game.main_path + '\\rec\\user\\invent.dat', 'r').read().split(';')
        except IOError:
            fi = open(self.game.main_path + '\\rec\\user\\invent.dat', 'w')
            fi.close()
            self.reload()
        for index, item in enumerate(self.contents):
            if not item:
                self.contents.pop(index)

    def add(self, item):
        fi = open(self.game.main_path + '\\rec\\user\\invent.dat', 'a')
        fi.write(str(item['name']) + ';')
        fi.close()
        self.reload()