import pygame
import pygame_gui
import networkx as nx
import re
import os


class RadiusCircle():
    def __init__(self, surface, radius, center):
        self.center = center
        self.radius = radius
        self.surface = surface
        # self.width = width
        # self.height = height

    def show(self):
        # surface = self.surface.copy()
        pygame.draw.circle(self.surface, (255, 0, 0),
                           self.center, self.radius, 1)


class Frame():
    def __init__(self, surface, keyFrame, delay, subFrame, content, highlightRate=0):
        self.surface = surface
        self.delay = delay
        self.subFrame = subFrame
        self.content = content
        self.highlightRate = highlightRate


class FrameList():
    def __init__(self, Algorithm_Class=None):
        self.frames = []
        self.content = []
        self.highlightRate = 0
        if Algorithm_Class == 0:
            with open("data/pseudoCode/adCS.html", "r") as cur_file:
                for line in cur_file:
                    self.content.append(line)
            for i in range(len(self.content)):
                self.content[i] = re.sub(r'\n', "", self.content[i])
        elif Algorithm_Class == 1:
            #BFS
            print("BFS in frame")
            pass
        elif Algorithm_Class == 2:
            #CS
            pass

    def highlightContent(self, highlight):
        # print(highlight)
        fileName = highlight[0]
        baseName = "data/pseudoCode/"
        highlightRange = [highlight[1], highlight[2]]
        self.content = []

        with open(os.path.join(baseName, fileName), "r") as cur_file:
            for line in cur_file:
                self.content.append(line)
        for i in range(len(self.content)):
            self.content[i] = re.sub(r'\n', "", self.content[i])
        for i in range(len(self.content)):
            if i in range(highlightRange[0], highlightRange[1]):
                self.content[i] = "<font color=#ff0000>" + \
                    self.content[i]+"</font>"
        self.highlightRate = highlightRange[0]/len(self.content)
        return self.content

    def append(self, surface, keyFrame=True, delay=100, curve=None, angle=None, descreasing=False, highlight=None):
        if highlight != None:
            self.content = self.highlightContent(highlight)
        print("content = ", self.content)
        frame = Frame(surface, keyFrame, delay, None,
                      self.content, self.highlightRate)
        if curve != None and angle != None:
            frame.subFrame = [curve, angle, descreasing]
        self.frames.append(frame)

    def __len__(self):
        return len(self.frames)
