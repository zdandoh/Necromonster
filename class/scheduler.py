import pygame

class Schedule():
    def __init__(self, game):
        """
        Class used to schedule ingame events. Executes code after a set time has elapsed.
        Code for scheduler must be written in the context of this class.
        """
        self.game = game
        self.schedule = []
        self.time = pygame.time.get_ticks()

    def add(self, code, time):
        """
        Called to add a new item to the scheduler. Requires code to be executed and duration until execution.
        """
        #don't forget to write code in the context of the scheduler class(s)!
        self.schedule.append([code, pygame.time.get_ticks() + time])

    def update(self):
        """
        Checks for any items that are due to execute.
        Exectues and removes any items with elapsed duration.
        """
        for index, item in enumerate(self.schedule):
            if pygame.time.get_ticks() >= item[1]:
                exec(item[0])
                self.schedule.pop(index)