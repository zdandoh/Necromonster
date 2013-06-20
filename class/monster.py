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
        monster['pos'] = pos
        monster['rect'] = monster['frames'].values()[0].get_rect()
        monster['movements'] = 0
        monster['moving'] = '' # 1, 2, 3, 4; up, left, down, right
        monster['face'] = 'front'
        monster['frameno'] = 1

        stats = self.getStats(difficulty)
        monster['level'] = stats[0]
        monster['health'] = stats[1]
        monster['attack'] = stats[2]
        monster['defense'] = stats[3]
        self.monsters.append(monster)

    def onMove(self, rect):
        for solid in self.game.solid_list:
            if solid == 'LINK':
                pass
            else:
                if rect.colliderect(solid):
                    return 1
        return 0


    def update(self):
        for index, monster in enumerate(self.monsters):
            new_monster = getattr(pathfind, monster['path'])(monster)
            if self.onMove(new_monster['rect']):
                pass
            else:
                self.monsters[index] = new_monster


    def blitMonsters(self):
        for index, monster in enumerate(self.monsters):
            self.monsters[index]['rect'] = self.game.screen.blit(monster['frames']['%s%s.png' % (monster['face'], monster['frameno'])], self.game.off(monster['pos']))