import os.path
import xml.etree.ElementTree as ET
from math import sqrt
from time import sleep
from pygame.image import load
from pygame.locals import *
from monster import Monster


class NPC(Monster):
    def __init__(self, game, name, pos, difficulty, pathfinding):
        """
        The basic NPC class. Characters that interact with the player.
        """
        self.greeting = '...'
        self.interacting = False
        self.text = NPCText(game, self, 'blacksmith')
        super(NPC, self).__init__(game, name, pos, difficulty, pathfinding)
        self.text.setGreeting(self.greeting)
        self.NPC = True
        self.head_icon = None
        self.thumbnail = load(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img', 'thumb.png')).convert_alpha()

    def execInfo(self):
        """
        Execute NPC info and get greeting.
        Overrides a function in the monster class.
        """
        fi_path = os.path.join(self.game.main_path, 'rec', 'npc', self.name, 'generate_xml.py')
        fi = open(fi_path, 'r').read()
        exec(fi)

    def loadFrames(self, name):
        """
        Loads all NPC frames that end in .png.
        Overrides a function in the monster class.
        """

        frames = {}
        for fi in os.listdir(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img')):
            if '.png' in fi:
                frames[fi] = load(os.path.join(self.game.main_path, 'rec', 'npc', name, 'img', fi)).convert_alpha()
        return frames

    def isPlayerClose(self, rng):
        """
        Checks if the player is within a certain radius of the NPC. Returns true or false.
        """
        close = False
        ppos = self.game.Player.getPos()
        npcpos = self.getPos()
        distance = sqrt(abs((ppos[0] - npcpos[0])**2 + (ppos[1] - npcpos[1])**2))
        if distance <= rng:
            close = True
        return close

    def update(self, index, ttime):
        """
        Updates the NPC. Does no pathfinding.
        Overrides a function in the monster class.
        """
        if self.interacting:
            self.text.interact()
        if not self.interacting:
            self.game.HUD.text_active = False
        if self.isPlayerClose(75) and not self.game.Player.head_drawn:
            self.game.Player.headDraw(self.text.getGreeting(), self.rect, off=False)
        if not self.isPlayerClose(75):
            self.interacting = False
            self.game.HUD.delPrompt()

    def blit(self):
        """
        overrides the blit method in the monster class to get rid of the uneeded health bar
        """
        self.game.screen.blit(self.frames['%s%s.png' % (self.face, self.frameno)], self.game.off([self.rect.x, self.rect.y]))


class NPCText(object):
    def __init__(self, game, npc, name):
        """
        Class for interacting with NPC speech XML and displaying it correctly.
        """
        self.name = name
        self.npc = npc
        self.game = game
        self.root = self.load()
        self.current_branch = self.root
        self.terminated = False

    def interact(self):
        """
        Called when the player should be speaking to the NPC
        """
        exec(self.getAction(self.current_branch))
        if not self.game.HUD.text_active and not self.game.HUD.body_text[0]:
            self.game.HUD.makePrompt(self)
        if not self.terminated and self.game.HUD.prompt_result:
            self.current_branch = self.current_branch.find("op" + str(self.game.HUD.prompt_result))
        self.interacting = False

    def pickOption(self, index):
        """
        Called when the player clicks an option from the NPC
        """
        options = self.getOptions(self.current_branch)
        new_branch = options[index]
        self.current_branch = new_branch
        self.game.HUD.makePrompt(self)
        if len(self.getOptions(new_branch)) <= 0:
            self.reset()

    def reset(self):
        """
        Set the NPC text current branch back to the root to begin conversation anew
        """
        self.current_branch = self.root

    def setAction(self, branch, code):
        """
        Sets the action of a speech branch in XML
        """
        branch.attrib['action'] = code

    def setText(self, branch, text):
        """
        Sets the text of a branch in XML
        """
        branch.text = text

    def setGreeting(self, text):
        """
        Sets the greeting of a text branch in the NPC
        """
        child = ET.SubElement(self.root, "greeting")
        child.text = text
        return child

    def addOption(self, branch, label, text):
        """
        Adds a possible option to the NPC speech tree. Essentially adds a new branch in XML
        """
        options_used = self.getOptions(branch)
        child = ET.SubElement(branch, 'op' + str(len(options_used) + 1))
        child.text = text
        child.attrib['label'] = label
        return child

    def getAction(self, branch):
        """
        Gets the action of a speech branch in XML.
        """
        try:
            return branch.attrib['action']
        except KeyError:
            return ''

    def getText(self, branch):
        """
        Gets the text of a branch in XML
        """
        return branch.text

    def getOptions(self, branch):
        """
        Gets a possible option set for the NPC with argument of parent branch
        """
        children = branch.getchildren()
        return children

    def getLabel(self, branch):
        """
        Gets the label of an NPC text branch
        """
        try:
            return branch.attrib['label']
        except KeyError:
            return None

    def getGreeting(self):
        greeting = 'not set'
        child = self.root.find('greeting')
        if child is not None:  # can't just use if: child, apparently
            greeting = child.text
        return greeting

    def load(self):
        """
        Returns the root of the XML file
        """
        root = ET.Element('data')
        if os.path.exists(os.path.join('rec', 'npc', self.name, self.name + '.xml')):
            tree = ET.parse(self.name + '.xml')
            root = tree.getroot()
        return root

    def save(self):
        fi = open(self.name + '.xml', 'w')
        fi.write(ET.tostring(self.root))
        fi.close()