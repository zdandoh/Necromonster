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
        self.hitbox = 0
        self.link = 0
        self.moving = 0
        self.surface_list = []
        self.surface_paths = []
        self.hitbox_list = []
        self.link_list = []
        self.screen = pygame.display.set_mode((900, 650), 1, 32)

        self.font = pygame.font.SysFont(None, 20)

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
        if self.link:
            mpos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(self.link[0], self.link[1], mpos[0] - self.link[0], mpos[1] - self.link[1]), 3)
        if self.moving:
            self.screen.blit(self.surface_list[self.moving - 1][0], pygame.mouse.get_pos())
        for item in self.hitbox_list:
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(item[0][0], item[0][1], item[1][0] - item[0][0], item[1][1] - item[0][1]), 3)
        for item in self.link_list:
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(item[0][0], item[0][1], item[1][0] - item[0][0], item[1][1] - item[0][1]), 3)
        coords = self.font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255))
        self.screen.blit(coords, (0, 0))

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
        for index, item in enumerate(self.surface_list):
            posfi.write('SURFACE:%s:%s:ground%s\n' % (self.surface_paths[index], item[1], item[2]))
        for index, hitbox in enumerate(self.hitbox_list):
            send_tuple = str(tuple(hitbox[0]) + tuple([hitbox[1][0] - hitbox[0][0], hitbox[1][1] - hitbox[0][1]]))
            posfi.write('SOLID:%s\n' % send_tuple)
        for index, link in enumerate(self.link_list):
            send_tuple = str(tuple(link[0]) + tuple([link[1][0] - link[0][0], link[1][1] - link[0][1]]))
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
                elif event.key == K_l:
                    if self.link:
                        mpos = pygame.mouse.get_pos()
                        map = inputbox.ask(self.screen, 'Map to link')
                        ppos = inputbox.ask(self.screen, 'New player pos')
                        pface = inputbox.ask(self.screen, 'New player face')
                        self.link_list.append([list(self.link), mpos, map, ppos, pface])
                        self.link = 0
                    else:
                        self.link = pygame.mouse.get_pos()

Editor()