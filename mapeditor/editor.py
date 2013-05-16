import pygame
from pygame.locals import *
import sys
import inputbox
import os
import Image
import shutil

pygame.init()

class Editor():
	def __init__(self):
		self.bg = ''
		self.bg_path = ''
		self.hitbox = 0
		self.moving = 0
		self.surface_list = []
		self.surface_paths = []
		self.hitbox_list = []
		self.screen = pygame.display.set_mode((900, 650), 1, 32)

		while 1:
			self.eventLoop()
			self.Draw()


	def Draw(self):
		self.screen.fill((0, 0, 0))
		if self.bg:
			self.screen.blit(self.bg, [0, 0])
		for item in self.surface_list:
			self.screen.blit(item[0], item[1])
		if self.hitbox:
			mpos = pygame.mouse.get_pos()
			pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.hitbox[0], self.hitbox[1], mpos[0] - self.hitbox[0], mpos[1] - self.hitbox[1]), 3)
		if self.moving:
			self.screen.blit(self.surface_list[self.moving - 1][0], pygame.mouse.get_pos())
		for item in self.hitbox_list:
			pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(item[0][0], item[0][1], item[1][0] - item[0][0], item[1][1] - item[0][1]), 3)

		pygame.display.update()

	def Export(self):
		print 'Exporting...'
		mapname = inputbox.ask(self.screen, 'Map Name')
		try:
			shutil.rmtree(mapname)
		except Exception:
			print 'First time export'

		# mk dirs
		os.mkdir(mapname)
		os.mkdir(mapname + '/buildings')
		os.mkdir(mapname + '/solids')

		# generate hitboxes
		for index, item in enumerate(self.hitbox_list):
			dimen = [item[1][0] - item[0][0], item[1][1] - item[0][1]]
			self.getHitboxImage(dimen, mapname, index)

		# move over bg and other surfaces
		if self.bg:
			bg = open(self.bg_path, 'rb').read()
			f = open(mapname + '/' + self.bg_path, 'wb').write(bg)
		for path in self.surface_paths:
			img = open(path, 'rb').read()
			f = open(mapname + '/buildings/' + path, 'wb').write(img)

		#create positions.txt
		print 'creating positions.txt'
		posfi = open(mapname + '/positions.txt', 'a')
		for index, item in enumerate(self.surface_list):
			posfi.write('%s:%s\n' % (self.surface_paths[index], item[1]))
		for index, hitbox in enumerate(self.hitbox_list):
			posfi.write('solid_%s.png:%s\n' % (index, hitbox[0]))

		print 'Export done'
		

	def eventLoop(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_a:
					#add surface
					img = inputbox.ask(self.screen, 'Path to image')
					self.surface_paths.append(img)
					try:
						img = pygame.image.load(img).convert_alpha()
					except Exception:
						pass
					else:
						self.surface_list.append([img, [0, 0]])
				elif event.key == K_e:
					self.Export()
				elif event.key == K_b:
					self.bg_path = inputbox.ask(self.screen, 'Path to BG')
					try:
						img = pygame.image.load(self.bg_path).convert_alpha()
					except Exception:
						pass
					else:
						self.bg = img
				elif event.key == K_m:
					if self.moving:
						self.surface_list[self.moving - 1][1] = list(pygame.mouse.get_pos())
						self.moving = 0
					else:
						for index, item in enumerate(self.surface_list):
							surf = item[0].get_rect()
							surf.x = item[1][0]
							surf.y = item[1][1]
							if surf.collidepoint(pygame.mouse.get_pos()):
								self.moving = index + 1
				elif event.key == K_h:
					if self.hitbox:
						self.hitbox_list.append([list(self.hitbox), pygame.mouse.get_pos()])
						self.hitbox = 0
					else:
						self.hitbox = pygame.mouse.get_pos()

	def getHitboxImage(self, dimensions, mapname, index):
		img = Image.new('RGBA', dimensions)
		img.save(mapname + '/solids/solid_%s.png' % index, 'PNG')

Editor()