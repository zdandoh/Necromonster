import random
import math
from heapq import *
from pygame.rect import Rect
from pygame.time import get_ticks

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

def getSign(num):
    if not num:
        return 0
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

def neutral(monster, game):
    # 1, 2, 3, 4; up, left, down, right(s)
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

def still(monster, game):
    return monster

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

        if get_ticks() - monster.last_attack > monster.aspeed and game.Player.collides(monster.rect):
            #knockback
            game.Player.takeDamage(monster.attack)
            game.Player.can_move = 0
            game.Player.addPos(move)
            game.Player.player_state = 2.
            n_move = [3 * getSign(move[0]), 3 * getSign(move[1])]
            for i in xrange(monster.knockback):
                game.Scheduler.add('self.game.Player.addPos({}); self.game.Player.onMove({})'.format(n_move, n_move), i * 20)
            game.Player.addPos([-n_move[0], -n_move[1]])
            game.Scheduler.add('self.game.Player.can_move = 1', i * 20)
            monster.last_attack = get_ticks()
        if onMove(monster.rect, game):
            monster.rect.x -= move[0]
            monster.rect.y -= move[1]
    else:
        #calculate a new path
        if game.Player.getDistance(monster.rect) > 400:
            return neutral(monster, game)
        monster.player_place = game.Player.getNode()
        monster.path_found = list(reversed(astar(game.Grid.nodes, (monster.pos[0] / 10, monster.pos[1] / 10), monster.player_place, game)))
        monster.player_node_when_pathfound = game.Player.getNode()
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

def heuristic(a, b):
    """calculates the H cost using the Manhattan Method"""
    return 10*(abs(a[0] - b[0]) + abs(a[1] - b[1]))

def astar(array, start, goal, game):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    open_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    open_set.add(start)
    heappush(oheap, (fscore[start], start))
    
    while len(open_set):

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
            
        open_set.discard(current)
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if neighbor not in open_set or tentative_g_score < gscore.get(neighbor, 0):
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.add(neighbor)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False
