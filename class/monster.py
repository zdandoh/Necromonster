import pathfind
from os import listdir
from pygame.image import load
from pygame.rect import Rect

class Monster():
    def __init__(self, game):
        self.monsters = []
        self.monster_rects = []
        self.game = game

    def getStats(self, difficulty):
        # stat format [level, health, attack, defense]
        return [difficulty, difficulty * 5, difficulty, difficulty]

    def getRects(self):
        rects = []
        for monster in self.monsters:
            rects.append(monster['rect'])
        return rects

    def loadFrames(self, name):
        frames = {}
        for fi in listdir(self.game.main_path + '\\rec\\enemy\\%s' % name):
            frames[fi] = load(self.game.main_path + '\\rec\\enemy\\%s\\%s' % (name, fi)).convert_alpha()
        return frames


    def create(self, name, pos, difficulty, pathfinding):
        monster = {}
        monster['name'] = name
        monster['frames'] = self.loadFrames(name)
        monster['path'] = pathfinding
        monster['rect'] = monster['frames'].values()[0].get_rect()
        monster['rect'].x = pos[0]
        monster['rect'].y = pos[1]
        monster['movements'] = 0
        monster['moving'] = '' # 1, 2, 3, 4; up, left, down, right
        monster['face'] = 'front'
        monster['frameno'] = 1

        stats = self.getStats(difficulty)
        monster['level'] = stats[0]
        monster['health'] = stats[1]
        monster['attack'] = stats[2]
        monster['defense'] = stats[3]
        monster['loot'] = 'Iron Ingot'
        self.monsters.append(monster)

    def kill(self, index):
        monster = self.monsters[index]
        if monster['loot']:
            self.game.ItemHandler.load(monster['loot'], pos=[monster['rect'].x, monster['rect'].y], spin=1, world=1)
        del self.monsters[index]

    def update(self):
        for index, monster in enumerate(self.monsters):
            self.monsters[index] = getattr(pathfind, monster['path'])(monster, self.game)


    def blitMonsters(self):
        for index, monster in enumerate(self.monsters):
            self.game.screen.blit(monster['frames']['%s%s.png' % (monster['face'], monster['frameno'])], self.game.off([monster['rect'].x, monster['rect'].y]))