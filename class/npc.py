import os.path
import xml.etree.ElementTree as ET
from pygame.image import load
from monster import Monster


class NPC(Monster):
    def __init__(self, game, name, pos, difficulty, pathfinding):
        super(NPC, self).__init__(game, name, pos, difficulty, pathfinding)
        self.NPC = True
        self.head_icon = None

    def execInfo(self):
        pass

    def loadFrames(self, name):
        frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img')):
            if '.png' in fi:
                frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img', fi)).convert_alpha()
        return frames


class NPCText(object):
    def __init__(self, name):
        self.name = name
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