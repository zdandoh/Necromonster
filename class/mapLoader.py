from pygame.image import load as imageload
from pygame import rect
from ast import literal_eval
import os

def load(map_name, game, new_pos = 0, face = 0):
    surfaces = []
    game.links = []
    game.solid_list = []
    l = os.path.abspath(__file__).split('\\')
    l.pop()
    l.pop()
    main_direc = 'rec\\maps\\%s\\' % map_name

    if new_pos:
        game.Player.setPos(literal_eval(new_pos))
    if face:
        game.Player.setFace(face)

    # get dict from positions.txt
    pos_dict = {}
    positions = open(main_direc + 'positions.txt', 'r').read()
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
            game.Player.setPos(eval(line.split(':')[1]))
        elif 'SURFACE' in line:
            ln = line.split(':')
            pos_dict[ln[1]] = literal_eval(ln[2])
        elif 'SOLID' in line:
            ln = line.split(':')
            game.solid_list.append(rect.Rect(eval(ln[1])))
    surfaces.append('player')
    # load all buildings
    tile = imageload(main_direc + 'tile.png').convert()
    game.tile = [tile, tile.get_size()]
    for fi in os.listdir(main_direc + 'buildings\\'):
        surfaces.append([imageload(main_direc + 'buildings\\' + fi).convert_alpha(), pos_dict[fi], 3])
    return surfaces