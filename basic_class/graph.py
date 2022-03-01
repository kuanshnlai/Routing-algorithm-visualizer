import pygame
import pygame_gui
import networkx as nx
from basic_class.component import *

formats = {"normal": "node: {g.nodesInfo} edge: {g.edgesInfo}"}


class graph(nx.Graph):

    def __init__(self, width=800, height=550):
        super().__init__()
        self.nodeNum = 0
        self.edgeNum = 0
        self.nodesInfo = dict()
        self.edgesInfo = dict()
        self.is_compile = False
        self.width = width
        self.height = height
        self.nodeSize = 20
        self.parasList = {"Start": None, "Destination": None,
                          "Radius": None, "MinSize": None}

    def add_node(self, posX, posY, nodeID=None, color=(0, 0, 255)):

        if nodeID == None:
            nodeID = str(self.nodeNum)
        super().add_node(str(nodeID))
        if self.is_exist(str(nodeID)):
            print("Node already exist")
        else:
            self.nodesInfo[str(nodeID)] = {
                "PosX": posX, "PosY": posY, "Color": color}
            print("Add node success", str(nodeID))
        self.nodeNum += 1
        self.is_compile = False

    def add_edge(self, edge, weight=1, color=(0, 0, 0)):
        edge = (str(edge[0]), str(edge[1]))
        super().add_edge(*edge)
        self.edgesInfo[edge] = {"Weight": weight, "Color": color}
        self.is_compile = False

    def del_node(self, nodeID):
        nodeID = str(nodeID)
        if nodeID == self.parasList['Start']:
            self.parasList['Start'] = None
        if nodeID == self.parasList['Destination']:
            self.parasList['Destination'] = None
        try:
            super().remove_node(nodeID)
            self.nodesInfo.pop(nodeID)
            self.is_compile = False
        except:
            print(nodeID, "doesn't exist")
        try:
            self.remove_relative_edge(nodeID)
            self.is_compile = False
        except:
            print("Cannot remove relative edges")

    def del_edge(self, edge):
        edge = (str(edge[0]), str(edge[1]))
        try:
            if edge in self.edgesInfo:
                super().remove_edge(*edge)
                self.edgesInfo.pop(edge)
            elif (edge[1], edge[0]) in self.edgesInfo:
                super().remove_edge(edge[1], edge[0])
                self.edgesInfo.pop((edge[1], edge[0]))
            self.is_compile = False
        except:
            print("Edge doesn't exist")

    def remove_relative_edge(self, edge):
        finish = False
        while not finish:
            finish = True
            for e in self.edgesInfo:
                if not(e in self.edges or (e[0], e[1]) in self.edges):
                    self.edgesInfo.pop(e)
                    finish = False
                    break

    def clear(self):
        width, height = self.width, self.height
        super().clear()
        self.__init__(width, height)
        return self.draw()

    def draw_grid(self, surface, gap):
        for i in range(0, self.width, gap):
            pygame.draw.line(surface, (193, 193, 193),
                             (i, 0), (i, self.height))
        for i in range(0, self.height, gap):
            pygame.draw.line(surface, (193, 193, 193), (0, i), (self.width, i))

    def draw(self):
        # create an surface
        surface = pygame.Surface((self.width, self.height))
        surface.fill((255, 255, 255))
        self.draw_grid(surface, 50)

        # draw vertices on the surface
        for v in self.nodesInfo:
            # draw all vertices
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render(
                str(v), True, self.nodesInfo[v]['Color'], (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = self.nodesInfo[v]['PosX'], self.nodesInfo[v]['PosY']
            pygame.draw.circle(surface, self.nodesInfo[v]['Color'], (
                self.nodesInfo[v]['PosX'], self.nodesInfo[v]['PosY']), self.nodeSize, 1)
            surface.blit(text, textRect)

        # draw edges on the surface
        for e in self.edges:
            # draw all edges
            x1 = self.nodesInfo[e[0]]['PosX']
            y1 = self.nodesInfo[e[0]]['PosY']
            x2 = self.nodesInfo[e[1]]['PosX']
            y2 = self.nodesInfo[e[1]]['PosY']
            v = (x2-x1, y2-y1)
            vlen = (v[0]**2+v[1]**2)**0.5
            u = (v[0]/vlen, v[1]/vlen)
            d = (int(u[0]*self.nodeSize), int(u[1]*self.nodeSize))
            pygame.draw.line(surface, (0, 0, 0),
                             (x1+d[0], y1+d[1]), (x2-d[0], y2-d[1]), 1)

        return surface

    def compile_graph(self):
        self.is_compile = True

    def update_node_color(self, nodeID, newColor=(0, 0, 255)):

        try:
            self.nodesInfo[nodeID]['Color'] = newColor
            self.draw()
        except:
            print(nodeID, "doesn't exist")

    def update_edge_color(self, edge, newColor):
        try:
            self.edgesInfo[edge]['Color'] = newColor
            self.draw()
        except:
            print(edge, "doesn't exist")

    def update_edge_weight(self, edge, weight):
        try:
            self.edgesInfo[edge]['Weight'] = weight
            self.draw()
        except:
            print(edge, "doesn't exist")

    def is_exist(self, nodeID):
        return nodeID in self.nodesInfo

    def get_neighbor(self, nodeID):
        return list(self.adj[nodeID])

    def exist_edge(self, edge):
        if edge in self.edgesInfo:
            return True
        elif (edge[1], edge[0]) in self.edgesInfo:
            return True
        return False

    def is_empty(self):
        if len(self.nodes) == 0:
            return True
        return False

    def __str__(self):
        return "Node: {} \n".format(self.nodesInfo)+"Edge: {}\n".format(self.edgesInfo) +\
            "Node primitive: {}\n".format(
                self.nodes)+"Edge primitive: {}\n".format(self.edges)

    def set_parameter(self, key, newValue):
        self.parasList[key] = newValue
        self.is_compile = False

    def distance(self, NodeAID=None, NodeBID=None, PosA=None, PosB=None):
        if(NodeAID == None and NodeBID == None):
            x1 = PosA[0]
            y1 = PosA[1]
            x2 = PosB[0]
            y2 = PosB[1]
        else:
            x1 = self.nodesInfo[NodeAID]['PosX']
            y1 = self.nodesInfo[NodeAID]['PosY']
            x2 = self.nodesInfo[NodeBID]['PosX']
            y2 = self.nodesInfo[NodeBID]['PosY']
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    def get_longest_neighbor(self, node):
        neighbor = self.get_neighbor(node)
        maxDistance = 0
        maxNeighbor = None
        for i in neighbor:
            d = self.distance(node, i)
            if d > maxDistance:
                maxDistance = d
                maxNeighbor = i
        return maxNeighbor
