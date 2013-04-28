import pygame
from pygame.locals import *
import sys
import random

sys.path.append('class')

import mapLoader

pygame.init()

class Player():
	def __init__(self, game):
		self.game = game
		self.player = pygame.image.load('rec/char/back1.png')
		self.player_face = 'back' # this is the part of the player that you see
		self.player_state = 1.
		self.player_r = self.player.get_rect()

		self.player_r.x = 50
		self.player_r.y = 50

	def update(self):
		total_moved = [0, 0]
		if 1 in self.game.keys_pressed:
			if self.game.keys_pressed[K_w]:
				self.player_r.y += -2
				for rect in self.game.solid_list:
					if self.player_r.colliderect(rect): self.player_r.y -= -2
				self.player_face = 'back'
			if self.game.keys_pressed[K_a]:
				self.player_r.x += -2
				for rect in self.game.solid_list:
					if self.player_r.colliderect(rect): self.player_r.x -= -2
				self.player_face = 'left'
			if self.game.keys_pressed[K_s]:
				self.player_r.y += 2
				for rect in self.game.solid_list:
					if self.player_r.colliderect(rect): self.player_r.y -= 2
				self.player_face = 'front'
			if self.game.keys_pressed[K_d]:
				self.player_r.x += 2
				for rect in self.game.solid_list:
					if self.player_r.colliderect(rect): self.player_r.x -= 2
				self.player_face = 'right'

			self.player_state += 0.3
			if self.player_state >= 4:
				self.player_state = 1
			self.player = pygame.image.load('rec/char/%s%s.png' % (self.player_face, int(self.player_state)))
		if not self.game.keys_pressed[K_w] and not self.game.keys_pressed[K_a] and not self.game.keys_pressed[K_s] and not self.game.keys_pressed[K_d]:
				self.player_state = 1

	def addPos(self, move):
		self.player_r.x += move[0]
		self.player_r.y += move[1]

	def setPos(self, new):
		self.player_r.x = new[0]
		self.player_r.y = new[1]

	def blitPlayer(self):
		self.game.screen.blit(self.player, (self.player_r.x, self.player_r.y))


class Necro():
	def __init__(self):
		self.Player = Player(self)
		# initiate the clock and screen
		self.clock = pygame.time.Clock()
		self.last_tick = pygame.time.get_ticks()
		self.screen = pygame.display.set_mode([900, 650], 0, 32)
		self.DEBUG = 0

		# get the map that you are on
		self.blit_list = mapLoader.load('home', self)

		while 1:
			self.Loop()

	def Loop(self):
		# main game loop
		self.eventLoop()
		if pygame.time.get_ticks() - self.last_tick > 20:
			self.Tick()
			self.Draw()
		pygame.display.update()

	def eventLoop(self):
		# the main event loop, detects keypresses
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()

	def Tick(self):
		# updates to player location and animation frame
		self.keys_pressed = pygame.key.get_pressed()
		self.clock.tick()
		self.Player.update()

		self.last_tick = pygame.time.get_ticks()

	def Draw(self):
		solid_count = 0
		for surf in self.blit_list:
			if 'player' in surf:
				self.Player.blitPlayer()
			elif 'solid' in surf:
				self.solid_list[solid_count] = self.screen.blit(surf[0], surf[1])
				solid_count += 1
			else:
				self.screen.blit(surf[0], surf[1])

Necro()