from pygame.image import load as imageload
import os, random

def load(map_name, game):
	surfaces = []
	game.solid_list = []
	l = os.path.abspath(__file__).split('\\')
	l.pop()
	l.pop()
	main_direc = '\\'.join(l) + '\\rec\\maps\\%s\\' % map_name
	
	# load bg
	surfaces.append([imageload(main_direc + 'bg.png').convert(), [0, 0], 1])
	# get dict from positions.txt
	pos_dict = {}
	positions = open(main_direc + 'positions.txt', 'r').read()
	for line in positions.split('\n'):
		if not line:
			pass
		elif line.startswith('#'):
			pass
		elif 'SET_PLAYER' in line:
			game.Player.setPos(eval(line.split(':')[1]))
		else:
			ln = line.split(':')
			pos_dict[ln[0]] = eval(ln[1]) # this is very dangerous. get less lazy and remove.
	# load all solids
	for fi in os.listdir(main_direc + 'solids\\'):
		ident = random.randrange(1, 500000)
		load_result = imageload(main_direc + 'solids\\' + fi).convert_alpha()
		if game.DEBUG:
			load_result.fill((255, 0, 0))
		surfaces.append([load_result, pos_dict[fi], 'solid']) # the list format of a solid: [surface, position, type identifier]
		game.solid_list.append(game.screen.blit(load_result, pos_dict[fi]))
	surfaces.append('player')
	# load all buildings
	for fi in os.listdir(main_direc + 'buildings\\'):
		surfaces.append([imageload(main_direc + 'buildings\\' + fi).convert_alpha(), pos_dict[fi], 3])
	return surfaces