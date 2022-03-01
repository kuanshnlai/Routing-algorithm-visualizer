import pygame
import pygame_gui
import sys
import time
import threading
from basic_class.constantDef import *


class TextBox():
    def __init__(self, html_text, manager, rect, window_surface, parent_element=None, object_id=None, container=None):
        self.content = html_text
        self.manager = manager
        self.rect = rect
        self.parent_element = parent_element
        self.object_id = object_id
        self.container = container
        self.displayRegion = pygame_gui.elements.ui_text_box.UITextBox(
            html_text=self.content, manager=self.manager, relative_rect=self.rect, parent_element=self.parent_element, container=self.container, object_id=self.object_id)
        self.window_surface = window_surface
        self.manager.draw_ui(self.window_surface)

    def clear(self):
        self.content = ""
        self.update()

    def update(self):
        time_delta = pygame.time.Clock().tick(60)/1000
        self.displayRegion.kill()
        self.displayRegion = pygame_gui.elements.ui_text_box.UITextBox(
            html_text=self.content, manager=self.manager, relative_rect=self.rect, parent_element=self.parent_element, container=self.container, object_id=self.object_id)
        self.moveToBottom()
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()
        self.manager.update(time_delta)

    def appendContent(self, string):
        self.content += '<br>'+string
        self.update()
        # self.moveToBottom()

    def moveToBottom(self):
        if self.displayRegion.scroll_bar == None:
            return
        if self.displayRegion.scroll_bar:
            scroll_bar = self.displayRegion.scroll_bar
            scroll_bar.scroll_wheel_down = False
            scroll_bar.scroll_position += (250 * 1)
            scroll_bar.scroll_position = min(scroll_bar.scroll_position,
                                             scroll_bar.bottom_limit - scroll_bar.sliding_button.rect.height)
            x_pos = scroll_bar.rect.x + scroll_bar.shadow_width + scroll_bar.border_width
            y_pos = scroll_bar.scroll_position + scroll_bar.rect.y + scroll_bar.shadow_width + \
                scroll_bar.border_width + scroll_bar.button_height
            scroll_bar.sliding_button.set_position(
                pygame.math.Vector2(x_pos, y_pos))

            scroll_bar.start_percentage = scroll_bar.scroll_position / \
                scroll_bar.scrollable_height
        if not scroll_bar.has_moved_recently:
            scroll_bar.has_moved_recently = True

    def moveToPos(self, ratio):
        print(self.displayRegion.scroll_bar)
        if self.displayRegion.scroll_bar == None:
            return
        if self.displayRegion.scroll_bar:
            scroll_bar = self.displayRegion.scroll_bar
            scroll_bar.scroll_wheel_down = False
            scroll_bar.scroll_position = 0
            scroll_bar.scroll_position += (scroll_bar.bottom_limit*ratio)
            print(scroll_bar.scroll_position)
            scroll_bar.scroll_position = min(scroll_bar.scroll_position,
                                             scroll_bar.bottom_limit - scroll_bar.sliding_button.rect.height)
            x_pos = scroll_bar.rect.x + scroll_bar.shadow_width + scroll_bar.border_width
            y_pos = scroll_bar.scroll_position + scroll_bar.rect.y + scroll_bar.shadow_width + \
                scroll_bar.border_width + scroll_bar.button_height
            scroll_bar.sliding_button.set_position(
                pygame.math.Vector2(x_pos, y_pos))

            scroll_bar.start_percentage = scroll_bar.scroll_position / \
                scroll_bar.scrollable_height
        if not scroll_bar.has_moved_recently:
            scroll_bar.has_moved_recently = True

    def simpleProcessBar(self, finish):
        print("Some one called me")
        print("Process function", threading.get_ident())
        origin = self.content
        self.appendContent("Process")
        count = 0
        time_delta = pygame.time.Clock().tick(60)/1000
        while finish[0] != True:
            if count % 50 == 0:
                self.content = origin
                self.appendContent("Process")
            elif count % 5 == 0:
                self.content += "."
                self.update()
            count += 1
            # self.manager.process_events(event)

    def showContent(self):
        print("Content = ")
        print(self.content)
class TestScroll():
    def __init__(self, width, height, manager, object_id, parent_element, container):
        self.manager = manager
        self.object_id = object_id
        self.parent_element = parent_element
        self.container = container
        self.panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (0, 0), (width, height)), starting_layer_height=0, manager=self.manager, parent_element=self.parent_element, object_id=object_id, container=container)
        self.scroll_bar = None
        self.components = []
        self.width = width
        self.height = height
        self.count = 0
        self.offsetX = 0
        self.offsetY = 0
        self.bottom = height
        self.anchor = 0

    def process_events(self, event):
        if self.scroll_bar == None:
            return
        if self.scroll_bar.has_moved_recently:
            print("I move")
            print(self.scroll_bar.scroll_position)
            self.rebuild()
        self.rebuild()

    def addComponent(self):
        width = 100
        height = 50
        button1 = pygame_gui.elements.ui_button.UIButton(text=str(self.count), relative_rect=pygame.Rect(
            (self.offsetX, self.offsetY), (width, height)), container=self.panel, manager=self.manager)
        button2 = pygame_gui.elements.ui_button.UIButton(text=str(self.count), relative_rect=pygame.Rect(
            (self.offsetX+105, self.offsetY), (width, height)), container=self.panel, manager=self.manager)
        self.offsetY += height+5
        self.count += 2
        self.update()
        self.components.append((button1, button1.rect.x, button1.rect.y))
        self.components.append((button2, button2.rect.x, button2.rect.y))
        # self.rebuild()

    def cheat(self):
        for i in self.components:
            button = i[0]
            button.set_position((i[1], i[2]))

    def update(self):
        percent = self.anchor/self.offsetY
        if self.offsetY > self.bottom and self.scroll_bar == None:
            # create an scroll bar allow user to slip down
            offsetX = self.width-25
            offsetY = 0
            self.scroll_bar = pygame_gui.elements.ui_vertical_scroll_bar.UIVerticalScrollBar(
                relative_rect=pygame.Rect((offsetX, offsetY), (20, self.height)), manager=self.manager, visible_percentage=0.1, parent_element=self.panel, container=self.panel)
            print("Initial state")
            print(self.scroll_bar.sliding_button.rect)
            print(self.scroll_bar.scrollable_height)
            print(self.scroll_bar.button_height)
            print(self.scroll_bar.bottom_limit)
            print(self.scroll_bar.scroll_position)

    def rebuild(self):

        if self.scroll_bar == None:
            return
        percent = (self.scroll_bar.scroll_position) / \
            (self.scroll_bar.scrollable_height -
             self.scroll_bar.button_height)

        self.anchor = self.offsetY * percent - self.height
        if self.anchor < 0:
            self.anchor = 0
        for i in self.components:
            button = i[0]
            offsetX = i[1]
            offsetY = i[2]
            button.set_position((offsetX, offsetY-self.anchor))
        # print("rebuild")
        pygame.display.update()

    def showMe(self):
        if self.scroll_bar == None:
            print("No")
            return
        print(self.scroll_bar.scroll_position)
        print(self.scroll_bar.scrollable_height)
        print(self.scroll_bar.button_height)
        percent = (self.scroll_bar.scroll_position) / \
            (self.scroll_bar.scrollable_height)
        print(percent)


class Tracer():
    '''
    所有的component往下疊加，當移除component時下面的component會遞補上來
    '''

    def __init__(self, width, height, manager, object_id, parent_element, container):
        self.manager = manager
        self.object_id = object_id
        self.parent_element = parent_element
        self.container = container
        self.fixRegion = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (0, 0), (width, 30)), starting_layer_height=0, manager=self.manager, parent_element=self.parent_element, object_id=object_id, container=container)
        self.panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (0, 35), (width, height)), starting_layer_height=0, manager=self.manager, parent_element=self.parent_element, object_id=object_id, container=container)
        self.scroll_bar = None
        self.components = []
        self.width = width
        self.height = height
        self.count = 0
        self.offsetX = 0
        self.offsetY = 0
        self.bottom = height
        self.anchor = 0
        self.title = []

    def set_title(self, kinds, args):
        maxHeight = 0
        offsetX = 0  # offset都從0開始
        offsetY = 0
        for i in range(len(kinds)):
            height = args[i]['height']
            width = args[i]['width']
            maxHeight = max(height, maxHeight)
            text = args[i]['text']
            container = args[i]['container']
            self.addComponent(kinds[i], height=height, width=width,
                              offsetX=offsetX, offsetY=offsetY, text=text, container=self.fixRegion, array=self.title)
            offsetX += width

    def addOneLine(self, kinds, args):
        '''
        kinds 代表元件類別(順序排列)
        args 代表創建這些元件的參數(用字典來裝)
        '''
        maxHeight = 0
        offsetX = 0  # offset都從0開始
        offsetY = self.offsetY
        for i in range(len(kinds)):

            height = args[i]['height']
            maxHeight = max(height, maxHeight)
            width = args[i]['width']
            text = args[i]['text']
            container = args[i]['container']
            self.addComponent(kinds[i], height=height, width=width,
                              offsetX=offsetX, offsetY=offsetY, text=text, container=self.panel)
            offsetX += width
        self.offsetY += maxHeight + 5
        self.update()

    def addComponent(self, componentConstructor, height, width, offsetX, offsetY, text, container, array=None):

        rect = pygame.Rect((offsetX, offsetY), (width, height))
        component = componentConstructor(
            rect=rect, text=text, container=container)
        self.update()
        if array == None:
            self.components.append(
                (component, rect.x, rect.y, rect.width, rect.height))
        else:
            array.append((component, rect.x, rect.y, rect.width, rect.height))

    def button(self, rect, text, container):
        return pygame_gui.elements.UIButton(text=text, relative_rect=rect, container=container, parent_element=container, manager=self.manager)

    def label(self, rect, text, container):
        return pygame_gui.elements.UILabel(text=text, relative_rect=rect, container=container, parent_element=container, manager=self.manager)

    def kill(self):
        self.panel.kill()

    def clearContent(self):
        for i in self.components:
            self.removeComponent(i[0])

    def removeComponent(self, component):
        print("remove ", component[0].text)
        for i in self.components:
            if i == component:
                i[0].kill()
                self.components.remove(i)

    def process_events(self, event):

        if self.scroll_bar == None:
            return
        if self.scroll_bar.has_moved_recently:
            print("I move")
            print(self.scroll_bar.scroll_position)
            self.rebuild()

    def cheat(self):
        lab = self.label(pygame.Rect((0, 0), (self.width, 30)),
                         text="text", container=self.panel)

    def update(self):

        if self.offsetY > self.bottom and self.scroll_bar == None:
            # create an scroll bar allow user to slip down
            percent = self.anchor/self.offsetY
            offsetX = self.width-25
            offsetY = 0
            self.scroll_bar = pygame_gui.elements.ui_vertical_scroll_bar.UIVerticalScrollBar(
                relative_rect=pygame.Rect((offsetX, offsetY), (20, self.height)), manager=self.manager, visible_percentage=0.1, parent_element=self.panel, container=self.panel)
            print("Initial state")
            print(self.scroll_bar.sliding_button.rect)
            print(self.scroll_bar.scrollable_height)
            print(self.scroll_bar.button_height)
            print(self.scroll_bar.bottom_limit)
            print(self.scroll_bar.scroll_position)

    def rebuild(self):

        if self.scroll_bar == None:
            return

        percent = (self.scroll_bar.scroll_position) / \
            (self.scroll_bar.scrollable_height -
             self.scroll_bar.button_height)

        self.anchor = self.offsetY * percent - self.height
        print("offset = ", self.offsetY)
        print("percent = ", percent)
        print("anchor = ", self.anchor)
        if self.anchor < 0:
            self.anchor = 0
        for i in self.components:
            button = i[0]
            offsetX = i[1]
            offsetY = i[2]
            print(button.text, offsetX, offsetY-self.anchor)
            button.set_relative_position(
                (offsetX, offsetY-self.anchor))


class ArrayTracer(Tracer):
    '''
    目標:
        當狀態為正在進行animation操作時，我想要array tracer顯示目前的節點，節點的鄰居，目前的播放狀態
        當狀態為編輯階段我希望array tracer顯示所有的節點的狀態，包含節點位置，目前網路圖的參數狀態
    '''

    def __init__(self, width, height, manager, object_id, parent_element, container):
        super().__init__(width, height, manager, object_id,
                         parent_element, container)
        self.rowLabel = []

    def addNewRow(self, kinds, args):
        row = kinds[0]
        self.rowLabel.append(args[0]['text'])
        self.addOneLine(kinds, args)
    # def __init__(self):

    def removeRow(self, index):
        finish = False
        maxHeight = 0
        # for i in self.components:
        #     print(i[0].text, i[0].rect.y)

        if index < len(self.rowLabel) and index >= 0:
            name = self.rowLabel[index]
            for i in self.components:
                if i[0].text == name:
                    offsetY = i[0].rect.y
                    break
            self.rowLabel.pop(index)
            while(not finish):
                finish = True
                for i in self.components:
                    if i[0].rect.y == offsetY:
                        maxHeight = max(i[3], maxHeight)
                        self.removeComponent(i)
                        finish = False
                        break

        self.rearrange(offsetY, maxHeight)
        self.offsetY -= maxHeight

    def rearrange(self, offsetY, height):
        print("rearrange")
        for i in range(len(self.components)):
            component = self.components[i]
            if component[2] >= height:
                print("---------")
                print(component[0].text, " reset",
                      component[2], "to", component[2]-height)
                print(component)
                print(component[0].get_relative_rect())
                component[0].set_relative_position(
                    (component[1], component[2]-height))
                print(component[0].get_relative_rect())
                tmp = list(component)
                tmp[2] -= height
                self.components[i] = tuple(tmp)
                print(component[0].get_relative_rect(), component)
                print("---------")
