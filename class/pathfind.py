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
    return 10*(abs(a[0] - b[0]) + abs(a[1] - b[1]))

def getG(current, neighbor):
    vector_sub = [abs(neighbor[0] - current[0]), abs(neighbor[1] - current[1])]
    if sum(vector_sub) > 1:
        move_cost = 14
    else:
        move_cost = 10
    return move_cost

def astar(array, start, dest, game):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    close_set = set()
    open_set = set()

    came_from = {}

    gscore = {start : 0}
    fscore = {start : heuristic(start, dest)}
    lowest = []

    open_set.add(start)


    while len(open_set):
        lowest = [(fscore[point], point) for point in open_set] #make list of fscores and grab the lowest one
        lowest.sort()
        current = lowest[0][1]

        if current == dest: #check if path is done
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path

        open_set.discard(current) #drop current and place it in closed list
        close_set.add(current)

        for x, y in neighbors: #chack neighbors
            current_neighbor = current[0]+x , current[1]+y

            new_g = gscore[current] + getG(current, current_neighbor)

            if 0 <= current_neighbor[0] < array.shape[0]:
                if 0 <= current_neighbor[1] < array.shape[1]:
                    if array[current_neighbor[0]][current_neighbor[1]] == 1:
                        continue # solid obstacle
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if current_neighbor in close_set and new_g >= gscore.get(current_neighbor, 0):
                continue

            if current_neighbor not in open_set or new_g < gscore.get(current_neighbor, 0):
                came_from[current_neighbor] = current
                gscore[current_neighbor] = new_g
                fscore[current_neighbor] = new_g + getG(current, current_neighbor)
                open_set.add(current_neighbor)
    return False