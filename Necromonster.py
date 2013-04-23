import pygame
from pygame.locals import *
import sys
import random

pygame.init()

class Necro():
	def __init__(self):
		# initiate the clock and screen
		self.clock = pygame.time.Clock()
		self.last_tick = pygame.time.get_ticks()
		self.screen = pygame.display.set_mode([900, 650], 0, 32)

		# player setup
		self.player_l = [50, 50]
		self.player_face = 'back' # this is the part of the player that you see
		self.player_state = 1.

		# load all images
		self.bg = pygame.image.load('rec/map/tower_bg.png').convert()
		self.tower = pygame.image.load('rec/map/tower.png').convert_alpha()
		self.player = pygame.image.load('rec/char/front1.png')

		# get rect for images
		self.tower_r = self.tower.get_rect()
		self.player_r = self.player.get_bounding_rect()

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
		self.clock.tick()
		keys_pressed = pygame.key.get_pressed()
		total_moved = [0, 0]
		if 1 in keys_pressed:
			if keys_pressed[K_w]:
				self.player_l[1] += -2
				self.player_r.y += -2
				if self.player_r.colliderect(self.tower_r): self.player_l[1] -= -2
				self.player_face = 'back'
			if keys_pressed[K_a]:
				self.player_l[0] += -2
				self.player_r.x += -2
				if self.player_r.colliderect(self.tower_r): self.player_l[0] -= -2
				self.player_face = 'left'
			if keys_pressed[K_s]:
				self.player_l[1] += 2
				self.player_r.y += 2
				if self.player_r.colliderect(self.tower_r): self.player_l[1] -= 2
				self.player_face = 'front'
			if keys_pressed[K_d]:
				self.player_l[0] += 2
				self.player_r.x += 2
				if self.player_r.colliderect(self.tower_r): self.player_l[0] -= 2
				self.player_face = 'right'

			self.player_state += 0.3
			if self.player_state >= 4:
				self.player_state = 1
			self.player = pygame.image.load('rec/char/%s%s.png' % (self.player_face, int(self.player_state)))
		if not keys_pressed[K_w] and not keys_pressed[K_a] and not keys_pressed[K_s] and not keys_pressed[K_d]:
				self.player_state = 1

		self.last_tick = pygame.time.get_ticks()

	def Draw(self):
		self.screen.blit(self.bg, [0, 0])
		self.tower_r = self.screen.blit(self.tower, [430, 254])
		self.player_r = self.screen.blit(self.player, self.player_l)

Necro()