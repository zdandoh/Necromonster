import pygame 
import math
import random

class ParticleManager():
    def __init__(self, game):
        self.game = game
        self.spawners = []

    def new(self, pos, size=5, density=4, color=(255,255,255), speed=6, shape='circle'):
        new = ParticleSpawner(self, pos, size, density, color, speed, shape)
        self.spawners.append(new)

    def update(self):
        for spawner in self.spawners:
            if spawner.current > spawner.s_duration:
                self.spawners.remove(spawner)
            
            spawner.update()
            spawner.draw(self.game.screen)

class ParticleSpawner():
    def __init__(self, spawner, pos, size, density, color, speed, shape):
        self.spawner = spawner
        self.pos = pos
        self.shape = shape
        self.size = size
        self.density = density
        self.speed = speed
        self.s_duration = self.size*7
        self.p_duration = self.s_duration/(self.speed + (self.size/10))
        self.color = color
        
        self.current = 0

        self.particles = []

        for d in xrange(self.density*5):
            self.particles.append(self.createParticle())

    def getVector(self):
        speed = random.randrange(-self.speed*10, self.speed*10)/10
        
        distance = [random.randrange(-40,40)/10.0, random.randrange(-40,40)/10.0]

        try:
            norm = math.sqrt(distance[0] ** 2.0 + distance[1] ** 2.0)
            direction = [distance[0] / norm, distance[1] / norm]
            vector = [direction[0] * speed, direction[1] * speed]
        except ZeroDivisionError:
            vector = [self.speed]*2

        return vector

    def createParticle(self):
        #particle list item: [rect, birthtime, vector, size]
        rect = pygame.Rect((self.pos), ([self.size]*2))
        particle = [rect, 0, self.getVector(), self.size]
        return particle
        
    def update(self):
        self.current += 1
        if self.current < self.density:
            for d in xrange(self.density*5):
                self.particles.append(self.createParticle())

        for particle in self.particles:
            particle[1] += 1

            if particle[1] > self.p_duration:
                self.particles.remove(particle)
            
            if particle[1] > self.p_duration/4:
                particle[3] -= 1
            
            particle[0].x += particle[2][0]
            particle[0].y += particle[2][1]
            
            if particle[3] > 1:
                particle[0].size = [particle[3]]*2

    def draw(self, screen):
        for particle in self.particles:
            if self.shape == 'rect':
                pygame.draw.rect(screen, self.color, particle[0])
            else:
                pygame.draw.circle(screen, self.color, particle[0].topleft, particle[0].width)
