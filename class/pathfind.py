import random
from pygame.rect import Rect

def getRandDirec():
    direc = random.randrange(1, 5)
    if direc == 1:
        return 'back'
    elif direc == 2:
        return 'left'
    elif direc == 3:
        return 'front'
    elif direc == 4:
        return 'right'
    else:
        raise BaseException

def onMove(rect, game):
    for solid in game.solid_list + [game.Player.getRect()]:
        if solid == 'LINK':
            pass
        else:
            if rect.colliderect(solid):
                return 1
    return 0


def neutral(monster, game):
    # 1, 2, 3, 4; up, left, down, right
    if monster[0]:
        change = [0, 0]
        if monster[1] > 20:
            monster[0] = 0
            monster[1] = 0
        elif monster[0] == 'back':
            change = [0, -2]
        elif monster[0] == 'left':
            change = [-2, 0]
        elif monster[0] == 'front':
            change = [0, 2]
        elif monster[0] == 'right':
            change = [2, 0]
        else:
            raise BaseException
        temp_rect = Rect(monster[2])

        temp_rect.x += change[0]
        temp_rect.y += change[1]
        if onMove(temp_rect, game):
            pass
        else:
            monster[2] = temp_rect
        monster[1] += 1
    else:
        if random.randrange(0, 150) == 50:
            direc = getRandDirec()
            monster[3] = direc
            monster[0] = direc
    return monster