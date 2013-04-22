import spriteLoader

class Structure():
	def __init__(self, surface, solid, pos=[0, 0]):
		self.structure = {'solid': solid, 'surface': spriteLoader.load(surface), 'pos': pos}

	def move(self, add_coords):
		self.structure['pos'][0] += add_coords[0]
		self.structure['pos'][1] += add_coords[1]

	def setPos(self, new_coords):
		self.structure['pos'] = new_coords

	def update(self, rectlist):
		if self.structure['solid']:
			for rect in rectlist:
				#run collision detection here
				pass
