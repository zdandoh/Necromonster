import pygame
from pygame.transform import *
from math import *
import time

class Shadow():
    def __init__(self, game, surface, pos):
        self.game = game
        self.sun = [0, 650]
        self.center = self.game.center_point
        self.image = self.renderShadow(surface)
        self.og_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        self.og_rect = self.rect.copy()

    def renderShadow(self, surface):
        surface = surface.copy()
        alphas = pygame.surfarray.pixels_alpha(surface)
        pixels = pygame.PixelArray(surface)

        for x in xrange(surface.get_width()):
            for y in xrange(surface.get_height()):
                if alphas[x, y] != 0:
                    pixels[x, y] = (0,0,0,50)

        sub = pixels.make_surface()
        return sub

    def rotate(self):
        self.rect = self.og_rect
        self.image = self.og_image

        

        angle = degrees(atan2(self.center[0]-self.sun[0], self.center[1]-self.sun[1]))
        angle = 180 + angle

        #dist = hypot(self.og_rect.midbottom[0] - self.rect.center[0] , self.og_rect.midbottom[1] - self.rect.center[1])
        #x = dist * cos(angle);
        #y = dist * sin(angle);


        #self.rect.x, self.rect.y = x, y
        self.image = rotate(self.image, angle)


    def moveSun(self, mouse):
        self.sun[0] = mouse [0]

    def Draw(self, screen):
        screen.blit(self.image, (self.game.off(self.rect)))

    def update(self, screen):
        self.moveSun(pygame.mouse.get_pos())
        self.rotate()
        self.Draw(screen)



