from globals import *

def load(map_name, game, new_pos = 0, face = 0):
    surfaces = []
    game.links = []
    game.solid_list = []
    l = os.path.abspath(__file__).replace('\\', '/').split('/')
    l.pop()
    main_direc = 'rec/maps/%s/' % map_name.replace('\\', '/')

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
            game.Player.setPos(literal_eval(line.split(':')[1]))
        elif 'SURFACE' in line:
            ln = line.split(':')
            pos_dict[ln[1]] = ln
        elif 'SOLID' in line:
            ln = line.split(':')
            game.solid_list.append(pygame.rect.Rect(literal_eval(ln[1])))
    # load all buildings
    tile = pygame.image.load(main_direc + 'tile.png').convert()
    game.tile = [tile, tile.get_size()]
    for time in [1, 2]:
        for index, fi in enumerate(os.listdir(main_direc + 'buildings/')):
            if pos_dict[fi][3] == 'ground%s' % time:
                surfaces.append([pygame.image.load(main_direc + 'buildings/' + fi).convert_alpha(), literal_eval(pos_dict[fi][2]), 3])
        if time == 1:
            surfaces.append('player')
    game.ItemHandler.clear()
    return surfaces
