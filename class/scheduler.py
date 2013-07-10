import pygame

class Schedule():
    def __init__(self, game):
        self.game = game
        self.schedule = []
        self.time = pygame.time.get_ticks()

    def add(self, code, time):
        #don't forget to write code in the context of the scheduler class!
        self.schedule.append([code, pygame.time.get_ticks() + time])

    def update(self):
        for item in self.schedule:
            if pygame.time.get_ticks() <= item[1]:
                exec(item[0])