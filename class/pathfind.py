import random

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

def neutral(monster):
    # 1, 2, 3, 4; up, left, down, right
    pos = monster['pos']
    if monster['moving']:
        if monster['movements'] > 20:
            monster['moving'] = 0
            monster['movements'] = 0
        elif monster['moving'] == 'back':
            pos[1] += -2
        elif monster['moving'] == 'left':
            pos[0] += -2
        elif monster['moving'] == 'front':
            pos[1] += 2
        elif monster['moving'] == 'right':
            pos[0] += 2
        else:
            raise BaseException
        monster['movements'] += 1
    else:
        if random.randrange(0, 150) == 50:
            direc = getRandDirec()
            monster['face'] = direc
            monster['moving'] = direc
    monster['pos'] = pos
    return monster