import os.path
import xml.etree.ElementTree as ET
from math import sqrt
from pygame.image import load
from monster import Monster


class NPC(Monster):
    def __init__(self, game, name, pos, difficulty, pathfinding):
        self.greeting = '...'
        self.text = NPCText(self, 'blacksmith')
        super(NPC, self).__init__(game, name, pos, difficulty, pathfinding)
        self.text.setGreeting(self.greeting)
        self.NPC = True
        self.head_icon = None

    def execInfo(self):
        # obtains greeting
        fi_path = os.path.join(self.game.main_path, 'rec', 'npc', self.name, 'generate_xml.py')
        fi = open(fi_path, 'r').read()
        exec(fi)

    def loadFrames(self, name):
        frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img')):
            if '.png' in fi:
                frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img', fi)).convert_alpha()
        return frames

    def isPlayerClose(self, rng):
        close = False
        ppos = self.game.Player.getPos()
        npcpos = self.getPos()
        distance = sqrt(abs((ppos[0] - npcpos[0])**2 + (ppos[1] - npcpos[1])**2))
        if distance <= rng:
            close = True
        return close

    def update(self, index, ttime):
        if self.isPlayerClose(75) and not self.game.Player.head_drawn:
            self.game.Player.headDraw(self.text.getGreeting(), self.rect, off=False)


class NPCText(object):
    def __init__(self, npc, name):
        self.name = name
        self.npc = npc
        self.root = self.load()
        self.current_branch = self.root
        self.terminated = False

    def interact(self):
        print self.getText(self.current_branch)
        exec(self.getAction(self.current_branch))
        options = self.getOptions(self.current_branch)
        for op_no, option in enumerate(options):
            print str(op_no + 1) + ': ' + self.getLabel(option)
        if not self.terminated:
            result = input('Choice: ')
            self.current_branch = self.current_branch.find("op" + str(result))
        if not self.terminated:
            self.interact()

    def setAction(self, branch, code):
        branch.attrib['action'] = code

    def setText(self, branch, text):
        branch.text = text

    def setGreeting(self, text):
        child = ET.SubElement(self.root, "greeting")
        child.text = text
        return child

    def addOption(self, branch, label, text):
        options_used = self.getOptions(branch)
        child = ET.SubElement(branch, 'op' + str(len(options_used) + 1))
        child.text = text
        child.attrib['label'] = label
        return child

    def getAction(self, branch):
        try:
            return branch.attrib['action']
        except KeyError:
            return ''

    def getText(self, branch):
        return branch.text

    def getOptions(self, branch):
        children = branch.getchildren()
        return children

    def getLabel(self, branch):
        return branch.attrib['label']

    def getGreeting(self):
        greeting = 'not set'
        child = self.root.find('greeting')
        if child is not None:  # can't just use if: child, apparently
            greeting = child.text
        return greeting

    def load(self):
        root = ET.Element('data')
        if os.path.exists(os.path.join('rec', 'npc', self.name, self.name + '.xml')):
            tree = ET.parse(self.name + '.xml')
            root = tree.getroot()
        return root

    def save(self):
        fi = open(self.name + '.xml', 'w')
        fi.write(ET.tostring(self.root))
        fi.close()