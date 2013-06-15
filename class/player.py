from globals import *

class Player():
    def __init__(self, game):
        self.game = game
        self.player = pygame.image.load('rec\\char\\back1.png')
        self.head_font = pygame.font.Font('rec\\font\\p_head.ttf', 15)
        self.player_face = 'back'  # this is the part of the player that you see
        self.player_state = 1.
        self.head_drawn = 0
        self.player_r = self.player.get_rect()
        self.player_dims = self.player.get_size()

        self.player_r.x = 450
        self.player_r.y = 528

    def update(self):
        #Update player position based on keypresses
        if 1 in self.game.keys_pressed:
            if self.game.keys_pressed[K_w]:
                self.player_r.y += -2
                self.onMove(1, -2)
                self.player_face = 'back'
            if self.game.keys_pressed[K_a]:
                self.player_r.x += -2
                self.onMove(0, -2)
                self.player_face = 'left'
            if self.game.keys_pressed[K_s]:
                self.player_r.y += 2
                self.onMove(1, 2)
                self.player_face = 'front'
            if self.game.keys_pressed[K_d]:
                self.player_r.x += 2
                self.onMove(0, 2)
                self.player_face = 'right'

            self.player_state += 0.15
            if self.player_state >= 4:
                self.player_state = 1
            self.player = pygame.image.load('rec/char/%s%s.png' % (self.player_face, int(self.player_state)))
        if not self.game.keys_pressed[K_w] and not self.game.keys_pressed[K_a] and not self.game.keys_pressed[K_s] and not self.game.keys_pressed[K_d]:
            self.player_state = 1

    def onMove(self, pos, offset, link_count = 0):
        #Collision detection run on movement
        for rect in self.game.solid_list:
            link_active = 0
            if 'LINK' in rect:
                link = self.game.links[link_count]
                rect = literal_eval(link[1])
                link_count += 1
                link_active = 1
            if self.player_r.colliderect(rect):
                if link_active:
                    self.game.blit_list = mapLoader.load(link[2], self.game, new_pos = link[3], face = link[4])
                else:
                    if pos:
                        self.player_r.y -= offset
                    elif not pos:
                        self.player_r.x -= offset

    def headDraw(self, text, dur=3):
        #Draw text at head of player
        font_render = self.head_font.render(text, True, (255, 255, 255))
        self.head_drawn = [font_render, self.game.off([self.player_r.x - (self.player_dims[0] / 2), self.player_r.y - 25]), time() + dur]

    def addPos(self, move):
        self.player_r.x += move[0]
        self.player_r.y += move[1]

    def collides(self, rect):
        return self.player_r.colliderect(rect)

    def setPos(self, new):
        self.player_r.x = new[0]
        self.player_r.y = new[1]

    def getPos(self, offset=[0, 0]):
        return [self.player_r.x + offset[0], self.player_r.y + offset[1]]

    def setFace(self, face, state=1):
        self.player_face = pygame.image.load('rec/char/%s%s.png' % (face, state))

    def blitPlayer(self):
        #Draws player and head text if it exists
        if self.head_drawn:
            if self.head_drawn[2] < time():
                self.head_drawn = 0
            else:
                self.game.screen.blit(self.head_drawn[0], self.head_drawn[1])
        self.game.screen.blit(self.player, self.game.off([self.player_r.x, self.player_r.y]))