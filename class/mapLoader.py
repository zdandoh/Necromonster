from pygame.image import load as imageload
from pygame import rect
import os

def load(map_name, game):
    surfaces = []
    links = []
    game.solid_list = []
    l = os.path.abspath(__file__).split('\\')
    l.pop()
    l.pop()
    main_direc = '\\'.join(l) + '\\rec\\maps\\%s\\' % map_name
    
    # load bg
    surfaces.append([imageload(main_direc + 'bg.png').convert_alpha(), [0, 0], 1])
    # get dict from positions.txt
    pos_dict = {}
    positions = open(main_direc + 'positions.txt', 'r').read()
    for line in positions.split('\n'):
        if not line:
            pass
        elif line.startswith('#'):
            pass
        elif 'NEWLINK' in line:
            line_bits = line.split(':')
        elif 'SET_PLAYER' in line:
            game.Player.setPos(eval(line.split(':')[1]))
        elif 'SURFACE' in line:
            ln = line.split(':')
            pos_dict[ln[1]] = eval(ln[2]) # this is very dangerous. get less lazy and remove.
        elif 'SOLID' in line:
            ln = line.split(':')
            game.solid_list.append(rect.Rect(eval(ln[1])))
    surfaces.append('player')
    # load all buildings
    for fi in os.listdir(main_direc + 'buildings\\'):
        surfaces.append([imageload(main_direc + 'buildings\\' + fi).convert_alpha(), pos_dict[fi], 3])
    return surfaces