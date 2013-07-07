import random
import math
import time
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
    if monster.moving:
        change = [0, 0]
        if monster.movements > 20:
            monster.moving = 0
            monster.movements = 0
        elif monster.moving == 'back':
            change = [0, -2]
        elif monster.moving == 'left':
            change = [-2, 0]
        elif monster.moving == 'front':
            change = [0, 2]
        elif monster.moving == 'right':
            change = [2, 0]
        else:
            raise BaseException
        temp_rect = Rect(monster.rect)

        temp_rect.x += change[0]
        temp_rect.y += change[1]
        if onMove(temp_rect, game):
            pass
        else:
            monster.rect = temp_rect
        monster.movements += 1
    else:
        if random.randrange(0, 150) == 50:
            direc = getRandDirec()
            monster.face = direc
            monster.moving = direc
    return monster

def getSign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

def aggressive(monster, game):
    if monster.path_progress:
        move = monster.path_progress.pop()
        monster.rect.x += move[0]
        monster.rect.y += move[1]
        
        if not move[0] and move[1] <= 0:
            monster.face = 'back'
        elif move[0] <= 0 and not move[1]:
            monster.face = 'left'
        elif not move[0] and move[1] >= 0:
            monster.face = 'front'
        elif move[0] >= 0 and not move[1]:
            monster.face = 'right'
            
        if onMove(monster.rect, game):
            monster.rect.x -= move[0]
            monster.rect.y -= move[1]
    else:
        #calculate a new path
        if game.Player.getDistance(monster.rect) > 400:
            return neutral(monster, game)
        monster.player_place = game.Player.getNode()
        s = time.time()
        monster.path_found = astar(game.Grid.nodes, (monster.pos[0] / 10, monster.pos[1] / 10), monster.player_place, game)
        monster.player_node_when_pathfound = game.Player.getNode()
        print time.time() - s
        convertPath(monster)
        return aggressive(monster, game)
    return monster

def convertPath(monster):
    monster.path_progress = []
    last_node = monster.getNode()
    while monster.path_found:
        next_node = list(monster.path_found.pop(0))
        node_diff = [(next_node[0] - last_node[0]) * 10, (next_node[1] - last_node[1]) * 10]
        remainders = [(abs(node_diff[0]) % monster.speed) * getSign(node_diff[0]), (abs(node_diff[1]) % monster.speed) * getSign(node_diff[1])]
        x_moves = [monster.speed * getSign(node_diff[0]) for _ in xrange(int(abs(math.floor(node_diff[0] / monster.speed))))]
        y_moves = [monster.speed * getSign(node_diff[1]) for i in xrange(int(abs(math.floor(node_diff[1] / monster.speed))))]
        if getSign(node_diff[1]) < 0:
            y_moves.pop()
        x_moves.append(remainders[0])
        y_moves.append(remainders[1])
        while len(x_moves) < len(y_moves):
            x_moves.append(0)
        while len(x_moves) > len(y_moves):
            y_moves.append(0)
        monster.node_progress = zip(x_moves, y_moves)
        monster.path_progress += monster.node_progress
        last_node = next_node
    monster.path_progress.reverse()

def astar(m, startp, endp, game):
    width, height = game.Grid.bounds
    start_x, start_y = startp
    end_x, end_y = endp
    node = [None, start_x, start_y, 0, abs(end_x - start_x) + abs(end_y - start_y)]
    closed_list = [node]
    c_list = {}
    c_list[start_y * width + start_x] = node
    k = 0
    while c_list:
        node = closed_list.pop(0)
        x = node[1]
        y = node[2]
        l = node[3] + 1
        k += 1
        if k & 1:
            neighbours = ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y))
        else:
            neighbours = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        for nx, ny in neighbours:
            if nx == end_x and ny == end_y:
                path = [(end_x, end_y)]
                while node:
                    path.append((node[1], node[2]))
                    node = node[0]
                return list(reversed(path))
            if 0 <= nx < width and 0 <= ny < height and m[ny][nx] == 0:
                if ny * width + nx not in c_list:
                    nn = (node, nx, ny, l, l + abs(nx - end_x) + abs(ny - end_y))
                    c_list[ny * width + nx] = nn
                    #adding to closelist ,using binary heap
                    nni = len(closed_list)
                    closed_list.append(nn)
                    while nni:
                        i = (nni - 1) >> 1
                        if closed_list[i][4] > nn[4]:
                            closed_list[i], closed_list[nni] = nn, closed_list[i]
                            nni = i
                        else:
                            break
    return 0