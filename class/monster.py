import pathfind
import os
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
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'enemy', name)):
            frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'enemy', name, fi)).convert_alpha()
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
        monster['hp'] = stats[1]
        monster['attack'] = stats[2]
        monster['defense'] = stats[3]
        monster['loot'] = 'Iron Ingot'
        self.monsters.append(monster)

    def kill(self, index, drop=1):
        monster = self.monsters[index]
        if monster['loot'] and drop == 1:
            self.game.ItemHandler.load(monster['loot'], pos=[monster['rect'].x, monster['rect'].y], spin=1, world=1)
        del self.monsters[index]

    def attack(self, index, damage):
        monster = self.monsters[index]
        damage -= monster['defense']
        if damage <= 0:
            damage = 1
        monster['hp'] -= damage
        self.monsters[index]['hp'] = monster['hp']
        if monster['hp'] <= 0:
            self.kill(index)

    def update(self):
        for index, monster in enumerate(self.monsters):
            self.monsters[index] = getattr(pathfind, monster['path'])(monster, self.game)


    def blitMonsters(self):
        for index, monster in enumerate(self.monsters):
            self.game.screen.blit(monster['frames']['%s%s.png' % (monster['face'], monster['frameno'])], self.game.off([monster['rect'].x, monster['rect'].y]))