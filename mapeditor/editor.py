import pygame
from pygame.locals import *
import sys
import inputbox
import os
import shutil

pygame.init()

class Editor():
    def __init__(self):
        self.bg = ''
        self.bg_path = ''
        self.bounds = [1000, 1000]
        self.hitbox = 0
        self.link = 0
        self.moving = 0
        self.surface_list = []
        self.surface_paths = []
        self.hitbox_list = []
        self.link_list = []
        self.movebox = [0, 0]
        self.screen = pygame.display.set_mode((900, 650), 1, 32)

        self.font = pygame.font.SysFont(None, 20)

        while 1:
            self.eventLoop()
            self.Tick()
            self.Draw()

    def Tick(self):
        self.keys_pressed = pygame.key.get_pressed()
        if 1 in self.keys_pressed:
            if self.keys_pressed[K_UP]:
                self.movebox[1] += -1
            if self.keys_pressed[K_LEFT]:
                self.movebox[0] += -1
            if self.keys_pressed[K_DOWN]:
                self.movebox[1] += 1
            if self.keys_pressed[K_RIGHT]:
                self.movebox[0] += 1

    def Draw(self):
        self.screen.fill((0, 0, 0))
        if self.bg:
            self.screen.blit(self.bg, self.off([0, 0]))
        for item in self.surface_list:
            self.screen.blit(item[0], self.off(item[1]))
        if self.hitbox:
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((self.hitbox),([pygame.mouse.get_pos()[0]-self.hitbox[0],pygame.mouse.get_pos()[1]-self.hitbox[1]])), 3)
        if self.link:
           pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect((self.link), ([pygame.mouse.get_pos()[0] - self.link[0], pygame.mouse.get_pos()[1] - self.link[1]])), 3)

        if self.moving:
            self.screen.blit(self.surface_list[self.moving - 1][0], (pygame.mouse.get_pos()))
        for item in self.hitbox_list:
            rectloc = self.off([item[0][0], item[0][1]])
            rectexten = [item[1][0], item[1][1]]
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(rectloc, rectexten), 3)
        for item in self.link_list:
            rectloc = self.off([item[0][0][0], item[0][0][1]])
            rectexten = [item[0][1][0], item[0][1][1]]
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(rectloc, rectexten), 3)
        mpos = self.font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255))
        coords = self.font.render(str(self.movebox), True, (255, 255, 255))
        self.screen.blit(coords, (0, 0))
        self.screen.blit(mpos, (0, 15))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.off([0, 0]), self.bounds), 2)
        pygame.draw.circle(self.screen, (0, 255, 0), self.off([0, 0]), 10)

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

        # move over bg and other surfaces
        if self.bg:
            bg = open(self.bg_path, 'rb').read()
            f = open(mapname + '/' + 'tile.png', 'wb').write(bg)
        for path in self.surface_paths:
            img = open(path, 'rb').read()
            f = open(mapname + '/buildings/' + path, 'wb').write(img)

        #create positions.txt
        print 'creating positions.txt'
        posfi = open(mapname + '/positions.txt', 'a')
        #write all basic info
        posfi.write('''#INFO:
#LINK:(RECT):NEWMAP:PLAYERFACE:PLAYERCOORDS

''')
        posfi.write('BOUNDS:%s\n' % self.bounds)
        for index, item in enumerate(self.surface_list):
            posfi.write('SURFACE:%s:%s:ground%s\n' % (self.surface_paths[index], item[1], item[2]))
        for index, hitbox in enumerate(self.hitbox_list):
            send_tuple = '%s,%s,%s,%s' %((hitbox[0][0]),(hitbox[0][1]),(hitbox[1][0]), (hitbox[1][1]))
            #send_tuple.x -= self.movebox[0]
            #send_tuple.y -= self.movebox[1]
            posfi.write('SOLID:%s\n' % send_tuple)
        for index, link in enumerate(self.link_list):
            send_tuple = '%s,%s,%s,%s'%((link[0][0][0]),(link[0][0][1]),(link[0][1][0]), (link[0][1][1]))
            #send_tuple.x -= self.movebox[0]
            #send_tuple.y -= self.movebox[1]
            posfi.write('LINK:%s:%s:%s:%s\n' % (send_tuple, link[2], link[3], link[4]))
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
                    if os.path.exists(img):
                        ground = inputbox.ask(self.screen, 'Back or fore (1 / 2)')
                        img = pygame.image.load(img).convert_alpha()
                        self.surface_list.append([img, [0, 0], ground])
                    else:
                        pass
                elif event.key == K_e:
                    self.Export()
                elif event.key == K_b:
                    self.bg_path = inputbox.ask(self.screen, 'Path to BG')
                    if os.path.exists(self.bg_path):
                        img = pygame.image.load(self.bg_path).convert_alpha()
                        self.bg = img
                    else:
                        pass
                elif event.key == K_m:
                    if self.moving:
                        self.surface_list[self.moving - 1][1] = list(self.poff(pygame.mouse.get_pos()))
                        self.moving = 0
                    else:
                        for index, item in enumerate(self.surface_list):
                            surf = item[0].get_rect()
                            surf.x = item[1][0]
                            surf.y = item[1][1]
                            if surf.collidepoint(self.poff(pygame.mouse.get_pos())):
                                self.moving = index + 1
                elif event.key == K_h:
                    if self.hitbox:
                        self.hitbox_list.append(([self.poff(self.hitbox),([pygame.mouse.get_pos()[0]-self.hitbox[0],pygame.mouse.get_pos()[1]-self.hitbox[1]])]))
                        self.hitbox = 0
                    else:
                        self.hitbox = pygame.mouse.get_pos()
                elif event.key == K_l:
                    if self.link:
                        mpos = pygame.mouse.get_pos()
                        map = inputbox.ask(self.screen, 'Map to link')
                        ppos = inputbox.ask(self.screen, 'New player pos')
                        pface = inputbox.ask(self.screen, 'New player face')
                        lol = (self.poff(self.link),([pygame.mouse.get_pos()[0]-self.link[0],pygame.mouse.get_pos()[1]-self.link[1]]))
                        self.hitbox = 0
                        self.link_list.append([lol, mpos, map, ppos, pface])
                        self.link = 0
                    else:
                        self.link = pygame.mouse.get_pos()
                elif event.key == K_s:
                    # set boundaries
                    bx = inputbox.ask(self.screen, 'Border Length: ')
                    by = inputbox.ask(self.screen, 'Border Height: ')
                    self.bounds = [int(bx), int(by)]
                    print self.bounds

    def off(self, coords):
        newx = coords[0] - self.movebox[0]
        newy = coords[1] - self.movebox[1]
        return [newx, newy]

    def poff(self, coords):
        newx = coords[0] + self.movebox[0]
        newy = coords[1] + self.movebox[1]
        return [newx, newy]

Editor()
