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
    if monster['moving']:
        change = [0, 0]
        if monster['movements'] > 20:
            monster['moving'] = 0
            monster['movements'] = 0
        elif monster['moving'] == 'back':
            change = [0, -2]
        elif monster['moving'] == 'left':
            change = [-2, 0]
        elif monster['moving'] == 'front':
            change = [0, 2]
        elif monster['moving'] == 'right':
            change = [2, 0]
        else:
            raise BaseException
        temp_rect = Rect(monster['rect'])

        temp_rect.x += change[0]
        temp_rect.y += change[1]
        if onMove(temp_rect, game):
            pass
        else:
            monster['rect'] = temp_rect
        monster['movements'] += 1
    else:
        if random.randrange(0, 150) == 50:
            direc = getRandDirec()
            monster['face'] = direc
            monster['moving'] = direc
    return monster