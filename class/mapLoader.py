import pygame
import numpy

import os
from ast import literal_eval
from shadow import Shadow


class Grid():
    def __init__(self, game, bounds):
        """
        Class used for pathfinding. Keeps track of filled and empty 10x10 pixel nodes.
        Compresses the map into 10x10 nodes on loading.
        """
        self.game = game
        self.bounds = bounds
        screen = pygame.Surface(game.screen_res)
        for rect in game.solid_list:
            if rect != 'player' and rect != 'LINK':
                surf = pygame.Surface([rect.w + 30, rect.h + 30])
                surf.fill((255, 0, 0))
                screen.blit(surf, (rect.x - 20, rect.y - 20))
        self.grid = pygame.surfarray.pixels2d(screen)
        self.compress()

    def getPart(self, begin, dims):
        """
        Gets a slice of the nodes. Used for reducing load while pathfinding.
        """
        return self.nodes[begin[1]:begin[1] + dims[1], begin[0]:begin[0] + dims[0]]

    def getPix(self, x, y):
        """
        Return specific pixel from map surfarray
        """
        return self.grid[x][y]

    def setNode(self, x, y, val):
        """
        Sets a node in the pathfinding node map
        """
        self.nodes[y][x] = val

    def compress(self):
        """
        Compresses the map surfarray into nodes that represent 10x10 pixel areas
        Pretty optimized with numpy.
        """
        self.nodes = numpy.zeros([self.bounds[0] / 10 + 10, self.bounds[1] / 10 + 10], dtype='uint8')

        for row_index, row in enumerate(self.nodes):
            for node_index, node in enumerate(row):
                begin_x = node_index * 10
                begin_y = row_index * 10
                if numpy.count_nonzero(self.grid[begin_y:begin_y + 10, begin_x:begin_x + 10]): # temp fix by adding 10 nodes of wiggle room
                    self.nodes[node_index][row_index] = 1

def load(map_name, game, new_pos = 0, face = 0):
    """
    Load a map from a map folder. Returns a list of surfaces that are on the map.
    Parses the custom map format.
    Kinda messy.
    """
    game.EntityHandler.clear()
    surfaces = []
    shadow_check = 0
    game.links = []
    game.solid_list = []
    inside = 0
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
        elif 'BOUNDS' in line:
            ln = line.split(':')
            borders = literal_eval(ln[1])
        elif "INSIDE" in line:
            shadow_check = int(line.split(':')[1])
            game.INSIDE = shadow_check

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
    if not shadow_check:
        for surf in surfaces:
            if 'player' in surf:
                pass
            else:
                shad = Shadow(game, surf[0], surf[1])
                game.shadows.append(shad)

    game.blit_list = surfaces
    game.Grid = Grid(game, borders)
    return surfaces