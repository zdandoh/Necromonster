import pygame
import os
from ast import literal_eval

class Grid():
    def __init__(self, game):
        self.game = game
        screen = pygame.Surface(game.screen_res)
        for rect in game.solid_list:
            if rect != 'player' and rect != 'LINK':
                surf = pygame.Surface([rect.w + 30, rect.h + 30])
                surf.fill((255, 0, 0))
                screen.blit(surf, (rect.x - 20, rect.y - 20))
        self.grid = pygame.surfarray.array2d(screen)
        self.compress()

    def getPix(self, x, y):
        return self.grid[x][y]

    def setNode(self, x, y, val):
        self.nodes[y][x] = val

    def getNode(self, x, y):
        begin_x = x * 10
        begin_y = y * 10
        pix_gotten = 0
        block_volume = 0
        for y_count in xrange(10):
            for x_count in xrange(10):
                if self.getPix(begin_x + x_count, begin_y + y_count):
                    block_volume += 1
        return block_volume

    def compress(self):
        self.nodes = [0 for x in xrange(self.game.screen_res[0] / 10)]
        self.nodes = [list(self.nodes) for x in xrange(self.game.screen_res[1] / 10)]
        for row_index, row in enumerate(self.nodes):
            for node_index, node in enumerate(row):
                if self.getNode(node_index, row_index):
                    self.nodes[row_index][node_index] = 1

def load(map_name, game, new_pos = 0, face = 0):
    surfaces = []
    game.links = []
    game.solid_list = []
    l = os.path.abspath(__file__).replace('\\', '/').split('/')
    l.pop()
    main_direc = os.path.join(game.main_path, 'rec', 'maps', map_name)

    if new_pos:
        game.Player.setPos(literal_eval(new_pos))
    if face:
        game.Player.setFace(face)

    # get dict from positions.txt
    pos_dict = {}
    positions = open(os.path.join(main_direc, 'positions.txt'), 'r').read()
    for line in positions.split('\n'):
        if not line:
            pass
        elif line.startswith('#'):
            pass
        elif 'LINK' in line:
            line_bits = line.split(':')
            game.links.append(line_bits)
            game.solid_list.append('LINK')
        elif 'SET_PLAYER' in line:
            game.Player.setPos(literal_eval(line.split(':')[1]))
        elif 'SURFACE' in line:
            ln = line.split(':')
            pos_dict[ln[1]] = ln
        elif 'SOLID' in line:
            ln = line.split(':')
            game.solid_list.append(pygame.rect.Rect(literal_eval(ln[1])))

    # load all buildings
    tile = pygame.image.load(os.path.join(main_direc, 'tile.png')).convert()
    game.tile = [tile, tile.get_size()]
    for time in [1, 2]:
        for index, fi in enumerate(os.listdir(os.path.join(main_direc, 'buildings/'))):
            pos_dict[fi][3] = pos_dict[fi][3].replace('\r', '')
            if pos_dict[fi][3] == 'ground%s' % time:
                img = pygame.image.load(os.path.join(main_direc, 'buildings/', fi))
                surfaces.append([img.convert_alpha(), literal_eval(pos_dict[fi][2]), 3, pygame.mask.from_surface(img)])
        if time == 1:
            surfaces.append('player')
    game.EntityHandler.clear()
    game.blit_list = surfaces
    game.Grid = Grid(game)
    return surfaces