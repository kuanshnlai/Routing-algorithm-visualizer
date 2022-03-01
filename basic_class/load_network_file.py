import pygame
import pygame_gui
import json
from basic_class.graph import *
'''
Load network graph from file
'''


class File:
    def __init__(self, graph=None, JsonFile=None):
        self.graph = graph
        self.JsonFile = JsonFile

    def convertToJson(self):
        json = dict()
        try:
            json['Nodes'] = self.remap(self.graph.nodesInfo)
            json['Edges'] = self.remap(self.graph.edgesInfo)
            self.JsonFile = json
        except:
            print("Graph cannot convert to Json")

    def convertToGraph(self):
        g = graph()

        nodes = self.unmap(self.JsonFile['Nodes'])
        edges = self.unmap(self.JsonFile['Edges'])
        print(nodes)
        print(edges)
        try:

            for node in nodes:
                g.add_node(nodeID=node, posX=nodes[node]['PosX'],
                           posY=nodes[node]['PosY'], color=nodes[node]['Color'])
            for edge in edges:
                g.add_edge(
                    edge=edge, weight=edges[edge]['Weight'], color=edges[edge]['Color'])
            self.graph = g
        except:
            print("Cannot convert json file to graph")

    def remap(self, d):
        v = d.values()
        k = d.keys()
        k1 = [str(i) for i in k]
        return dict(zip(*[k1, v]))

    def unmap(self, d):
        v = d.values()
        k = d.keys()
        k1 = [eval(i) for i in k]
        return dict(zip(*[k1, v]))

    def __str__(self):
        try:
            graphDescribe = "Graph: \"Node\":{node},\"Edge\"{egde}".format(
                node=self.graph.nodesInfo, edge=self.graph.edgesInfo)
        except:
            graphDescribe = ''
        try:
            jsonFileDescirbe = "JsonFile:{File}".format(self.JsonFile)
        except:
            jsonFileDescirbe = ''

        return graphDescribe+jsonFileDescirbe

    def get_graph(self):
        return self.graph

    def get_jsonFile(self):
        return self.JsonFile


class LoadFileDialogWindow(pygame_gui.windows.ui_file_dialog.UIFileDialog):
    def __init__(self, manager, posx, posy, width, height):
        super().__init__(rect=pygame.Rect(
            (posx, posy), (width, height)), manager=manager, window_title='Load File...', initial_file_path='newdir', allow_existing_files_only=False)
        self.survive = True
        self.fileObj = None
        self.graph = None
        self.type = "Load File"
        self.is_valid = False

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self.load(event.text)
                print(self.fileObj)
                self.kill()
                self.survive = False
            if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                self.kill()
                self.survive = False
                self.is_valid = False

    def load(self, path):
        try:
            f = open(path, mode='r')
            result = json.load(f)
            self.fileObj = File(JsonFile=result)
            self.fileObj.convertToGraph()
            self.graph = self.fileObj.get_graph()
            self.is_valid = True
        except:
            result = ''
            print("Cannot open file")
            self.is_valid = False


class StoreFileDialogWindow(pygame_gui.windows.ui_file_dialog.UIFileDialog):
    def __init__(self, manager, posx, posy, width, height, graph):
        super().__init__(rect=pygame.Rect(
            (posx, posy), (width, height)), manager=manager, window_title='Store File...', initial_file_path='newdir', allow_existing_files_only=False)
        self.survive = True
        self.fileObj = File(graph=graph)
        self.type = "Store File"
        self.is_valid = False

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self.fileObj.convertToJson()
                self.store(event.text, self.fileObj.JsonFile)
                self.kill()
                self.survive = False
            if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                self.kill()
                self.survive = False
                self.is_valid = False

    def store(self, path, jsonFile):
        # print(json)
        # s = json.dumps(jsonFile)
        # print(s)
        try:
            with open(path, 'w') as f:
                json.dump(jsonFile, f, separators=(
                    ',\n', ': '), sort_keys=True, indent=4)
                self.is_valid = True
        except:
            print("Cannot store the file")
            self.is_valid = False
