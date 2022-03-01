import pygame
import pygame_gui
import threading
from pygame_gui.core import ObjectID
from basic_class.component import *
from basic_class.graph import *
from basic_class.pop_up_window import *
from basic_class.load_network_file import *
from basic_class.animation import *
from basic_class.algorithm import *
from basic_class.console import *
from basic_class.constantDef import *
HOMEBTNID = "#Home_button"
ROUTINGBTNID = "#Routing_button"
BTNSID = [HOMEBTNID, ROUTINGBTNID]
SELECTIONLISTID = ["#Option_"+str(i+700) for i in range(200)]

PLAYBTNID = "#Play_button"
PAUSEBTNID = "#Pause_button"
STOPBTNID = "#Stop_button"
PREVIOUSBTNID = "#Previous_button"
NEXTBTNID = "#Next_button"
BUILDBTNID = "#Build_button"
CLEARBTNID = "#Clear_button"
LOADFILEBTNID = "#Load_file_button"
STOREFILEBTNID = "#Store_file_button"
SETBTNID = "#Set_button"
SPEEDFASTBTNID = "#Plus_button"
SPEEDSLOWID = "#Minus_button"
ADDNODE = "#AddNode"
DELNODE = "#DelNode"
CONTENTPANELID = ""
MEDIASBTNID = [PLAYBTNID, PAUSEBTNID, STOPBTNID, PREVIOUSBTNID,
               NEXTBTNID, SETBTNID, SPEEDFASTBTNID, SPEEDSLOWID]


# Panel ID Define
SELECTIONPANELID = "#Selection_panel"
CONTROLPANELID = "#Control_panel"
GRAPHPANELID = "#Graph_panel"
ARRAYPANELID = "#Array_panel"
CONSOLEPANELID = "#Console_panel"
COMMANDLINEPANELID = "#Command_panel"
CONTENTPANELID = "#Content_panel"
PANELSID = [SELECTIONPANELID, CONTROLPANELID, GRAPHPANELID,
            ARRAYPANELID, CONSOLEPANELID, COMMANDLINEPANELID]

# State Number Define
HOMESTATE = 2000
ROUTINGSTATE = 2001
SELECTIONSTATE = [i+2000 for i in range(200)]


class GUI:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        # INITSTATE: Initial(Home Btn pressed)   ROUTINGSTATE: (Routing Btn pressed)
        self.btnState = HOMESTATE
        # INITSTATE: First option be selected (Default)
        self.selectionState = SELECTIONSTATE[0]
        # INITSTATE: No Graph
        self.mediaState = [INITSTATE, DEFAULTSTATE]
        self.finish = [True]
        self.width, self.height = width, height
        # Surface
        self.window_surface = pygame.display.set_mode(
            (self.width, self.height))
        self.backgroundColor = (81, 98, 111)
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(self.backgroundColor)
        self.manager = pygame_gui.UIManager(
            (width, height), 'data/themes/Button.json')
        self.newWindowSurvive = False
        self.newWindow = None

        self.clock = pygame.time.Clock()
        self.speed = 1.0
        self.create_all_elements()
        self.animation = None
        self.Algorithm_Class = BFS
        self.handlePanelLayout()
        self.mediaBtns = {(INITSTATE, DEFAULTSTATE):
                          {self.playbutton: 0, self.pausebutton: 0, self.stopbutton: 0, self.previousbutton: 0,
                           self.nextbutton: 0, self.clearbutton: 0, self.addnodebutton: 1, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 1,
                           self.storefilebutton: 1},
                          (NOTCOMPILESTATE, DEFAULTSTATE):
                          {self.playbutton: 0, self.pausebutton: 0, self.stopbutton: 0, self.previousbutton: 0,
                           self.nextbutton: 0, self.clearbutton: 1, self.addnodebutton: 1, self.deletenodebutton: 1, self.buildbutton: 1,
                           self.setpropertybutton: 1, self.loadfilebutton: 1,
                           self.storefilebutton: 1},
                          (COMPILESTATE, DEFAULTSTATE):
                          {self.playbutton: 1, self.pausebutton: 0, self.stopbutton: 0, self.previousbutton: 0,
                           self.nextbutton: 0, self.clearbutton: 1, self.addnodebutton: 1, self.deletenodebutton: 1, self.buildbutton: 0,
                           self.setpropertybutton: 1, self.loadfilebutton: 1,
                           self.storefilebutton: 1},
                          (PLAYSTATE, ONLYSTATE):
                          {self.playbutton: 0, self.pausebutton: 1, self.stopbutton: 1, self.previousbutton: 0,
                           self.nextbutton: 0, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PLAYSTATE, FIRSTSTATE):
                          {self.playbutton: 0, self.pausebutton: 1, self.stopbutton: 1, self.previousbutton: 0,
                           self.nextbutton: 1, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PLAYSTATE, INTERMIDIATESTATE):
                          {self.playbutton: 0, self.pausebutton: 1, self.stopbutton: 1, self.previousbutton: 1,
                           self.nextbutton: 1, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PLAYSTATE, LASTSTATE):
                          {self.playbutton: 0, self.pausebutton: 1, self.stopbutton: 1, self.previousbutton: 1,
                           self.nextbutton: 0, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PAUSESTATE, ONLYSTATE):
                          {self.playbutton: 1, self.pausebutton: 0, self.stopbutton: 1, self.previousbutton: 0,
                           self.nextbutton: 0, self.clearbutton: 0, self.addnodebutton: 1, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PAUSESTATE, FIRSTSTATE):
                          {self.playbutton: 1, self.pausebutton: 0, self.stopbutton: 1, self.previousbutton: 0,
                           self.nextbutton: 1, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PAUSESTATE, INTERMIDIATESTATE):
                          {self.playbutton: 1, self.pausebutton: 0, self.stopbutton: 1, self.previousbutton: 1,
                           self.nextbutton: 1, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          (PAUSESTATE, LASTSTATE):
                          {self.playbutton: 1, self.pausebutton: 0, self.stopbutton: 1, self.previousbutton: 1,
                           self.nextbutton: 0, self.clearbutton: 0, self.addnodebutton: 0, self.deletenodebutton: 0, self.buildbutton: 0,
                           self.setpropertybutton: 0, self.loadfilebutton: 0,
                           self.storefilebutton: 0},
                          }
        self.changed = False
        self.buildFinish = [False]
        self.buildPress = False
        self.PlayPress = False

    def create_all_elements(self):
        # panel size and pos

        self.selectPanelWidth, self.selectPanelHeight = 210, self.height
        self.controlPanelOffsetX, self.controlPanelOffsetY, self.controlPanelWidth, self.controlPanelHeight = 220, 50, 890, 80
        self.graphPanelOffsetX, self.graphPanelOffsetY, self.graphPanelWidth, self.graphPanelHeight = 220, 80, 890, 620
        self.arrayPanelOffsetX, self.arrayPanelOffsetY, self.arrayPanelWidth, self.arrayPanelHeight = 1120, 50, 400, 310
        self.consoleOffsetX, self.consoleOffsetY, self.consoleWidth, self.consoleHeight = 1120, 360, 400, 310
        self.commandLineOffsetX, self.commandLineOffsetY, self.commandLineWidth, self.commandLineHeight = 1120, 670, 400, 30
        self.contentOffsetX, self.contentOffsetY, self.contentWidth, self.contentHeight = 220, 50, 1290, 620
        # Option List
        self.optionList = {HOMESTATE: [
            "Guide"], ROUTINGSTATE: ["AdaptiveCS", "BFS", "CS", "Distance vector"]}
        # BTN
        self.HomeBtn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (210, 0), (100, 50)), text="Home", manager=self.manager, object_id=HOMEBTNID)
        self.HomeBtn.disable()
        self.routingBtn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (320, 0), (100, 50)), text="Routing", manager=self.manager, object_id=ROUTINGBTNID)
        self.BtnOfAll = [self.HomeBtn, self.routingBtn]
        # Panel Define
        self.selectListPanel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((0, 0), (self.selectPanelWidth, self.height)), manager=self.manager, starting_layer_height=1, object_id=SELECTIONPANELID)
        self.controlPanel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((self.controlPanelOffsetX, self.controlPanelOffsetY), (self.controlPanelWidth, self.controlPanelHeight)), manager=self.manager, starting_layer_height=1, object_id=CONTROLPANELID)
        self.graphPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (self.graphPanelOffsetX, self.graphPanelOffsetY), (self.graphPanelWidth, self.graphPanelHeight)), manager=self.manager, starting_layer_height=1, object_id=GRAPHPANELID)
        self.contentPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((self.contentOffsetX, self.contentOffsetY), (
            self.contentWidth, self.contentHeight)), manager=self.manager, starting_layer_height=1, object_id=CONTENTPANELID)
        self.arrayPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (self.arrayPanelOffsetX, self.arrayPanelOffsetY), (self.arrayPanelWidth, self.arrayPanelHeight)), manager=self.manager, starting_layer_height=1, object_id=ARRAYPANELID)
        self.tracer = ArrayTracer(width=self.arrayPanelWidth-5, height=self.arrayPanelHeight-35, manager=self.manager,
                                  object_id="#tracer", parent_element=self.arrayPanel, container=self.arrayPanel)
        self.consolePanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (self.consoleOffsetX, self.consoleOffsetY), (self.consoleWidth, self.consoleHeight)), manager=self.manager, starting_layer_height=1, object_id=CONSOLEPANELID)
        self.commandLinePanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
            (self.commandLineOffsetX, self.commandLineOffsetY), (self.commandLineWidth, self.commandLineHeight)), manager=self.manager, starting_layer_height=1, object_id=COMMANDLINEPANELID)

        # component of selection panel
        self.selectLabel = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.selectPanelWidth, 20)), manager=self.manager, parent_element=self.selectListPanel, container=self.selectListPanel, text="Selection")
        self.selectionList = pygame_gui.elements.ui_selection_list.UISelectionList(
            relative_rect=pygame.Rect((0, 20), (self.selectPanelWidth, self.height)), manager=self.manager, container=self.selectListPanel, item_list=self.optionList[self.btnState])
        # component of control panel
        self.playbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=PLAYBTNID, class_id="@Control_button"))
        self.pausebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (50, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=PAUSEBTNID, class_id="@Control_button"))

        self.stopbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (90, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=STOPBTNID, class_id="@Control_button"))

        self.previousbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (130, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=PREVIOUSBTNID, class_id="@Control_button"))

        self.nextbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (170, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=NEXTBTNID, class_id="@Control_button"))

        self.setpropertybutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (210, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=SETBTNID, class_id="@Control_button"))

        self.buildbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (250, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=BUILDBTNID, class_id="@Control_button"))

        self.clearbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (290, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=CLEARBTNID, class_id="@Control_button"))

        self.loadfilebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (330, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=LOADFILEBTNID, class_id="@Control_button"))
        self.storefilebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (370, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=STOREFILEBTNID, class_id="@Control_button"))
        self.addnodebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (400, 0), (70, 30)), text="Add Node", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=ADDNODE, class_id="@Control_button"))

        self.deletenodebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (480, 0), (100, 30)), text="Delete Node", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=DELNODE, class_id="@Control_button"))

        # self.speedtxtlabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        # (650, 5), (50, 20)), manager=self.manager, parent_element=self.controlPanel, container=self.controlPanel, text="Speed:")
        # self.speedlabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        # (700, 5), (30, 20)), manager=self.manager, parent_element=self.controlPanel, container=self.controlPanel, text=str(self.speed))
        # self.speedaddbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        # (740, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=SPEEDFASTBTNID, class_id="@Control_button"))
        # self.speedminusbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        # (780, 0), (30, 30)), text="", manager=self.manager, container=self.controlPanel, parent_element=self.controlPanel, object_id=ObjectID(object_id=SPEEDSLOWID, class_id="@Control_button"))

        self.BtnOfMedia = [self.playbutton, self.pausebutton, self.stopbutton, self.buildbutton,
                           self.nextbutton, self.previousbutton]

        # component of graph panel

        self.graph = graph(self.graphPanelWidth, self.graphPanelHeight)
        self.frame = self.graph.draw()
        self.graphLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
            (0, 0), (120, 20)), manager=self.manager, parent_element=self.graphPanel, container=self.graphPanel, text="Graph tracer")
        self.displayRegion = pygame.Surface(
            (self.graphPanelWidth, self.graphPanelHeight-30))
        self.displayRegion.blit(self.frame, (0, 0))
        self.graphRegion = pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect(
            (0, 30), (self.graphPanelWidth, self.graphPanelHeight-30)), manager=self.manager, container=self.graphPanel, parent_element=self.graphPanel, image_surface=self.displayRegion)

        # component of array panel
        # self.arrayLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        #     (0, 0), (120, 20)), manager=self.manager, parent_element=self.arrayPanel, container=self.arrayPanel, text="Array tracer")
        # component of commandLine panel
        # component of console panel
        fileContent = []
        base = "data/pseudoCode/"
        with open(os.path.join(base, "Guide.html")) as cur_file:
            for line in cur_file:
                fileContent.append(line)
        # print(fileContent)
        for i in range(len(fileContent)):
            fileContent[i] = re.sub(r'\n', "", fileContent[i])
        content = ""
        for line in fileContent:
            content += line

        contentRect = pygame.Rect(
            (0, 0), (self.contentWidth, self.contentHeight))
        self.contentRegion = TextBox(content, self.manager, contentRect, self.window_surface,
                                     parent_element=self.contentPanel, object_id="#content_region", container=self.contentPanel)
        self.consoleLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
            (0, 0), (80, 20)), manager=self.manager, parent_element=self.consolePanel, container=self.consolePanel, text="Console")
        self.console = TextBox(html_text="", manager=self.manager, rect=pygame.Rect((0, 20), (self.consoleWidth, self.consoleHeight-20)),
                               window_surface=self.window_surface, parent_element=self.consolePanel, object_id="#console", container=self.consolePanel)
        # self.test = pygame_gui.elements.ui_text_box.UITextBox(html_text="Init",relative_rect=pygame.Rect((20),()))
        self.panelOfAll = [self.selectListPanel, self.controlPanel,
                           self.graphPanel, self.arrayPanel, self.consolePanel, self.commandLinePanel, self.contentPanel]
        self.panelOfHome = [self.selectListPanel, self.contentPanel]
        print(self.console.displayRegion)
        self.panelOfRouting = [self.selectListPanel, self.controlPanel,
                               self.graphPanel, self.arrayPanel, self.consolePanel, self.commandLinePanel]

    def init_tracer(self):
        components = [self.tracer.label, self.tracer.label, self.tracer.label]
        args = [{'height': 30, 'width': 50, "text": 'Name', "container": self.tracer.panel}, {'height': 30, 'width': 100,
                                                                                              "text": 'Pos', "container": self.tracer.panel}, {'height': 30, 'width': 70, "text": 'State', "container": self.tracer.panel}]
        self.tracer.set_title(components, args)

    def update_tracer(self):
        for i in self.graph.nodesInfo:
            name = i
            pos = '('+str(self.graph.nodesInfo[i]['PosX']) + \
                ' , ' + str(self.graph.nodesInfo[i]['PosY'])+')'
            if name in self.tracer.rowLabel:
                pass
            else:
                kinds = [self.tracer.label,
                         self.tracer.label]
                args = [{'height': 30, 'width': 50, 'text': name, 'container': self.tracer.panel}, {'height': 30, 'width': 100, 'text': pos,
                                                                                                    'container': self.tracer.panel}]
                self.tracer.addNewRow(kinds, args)

    def kill(self):
        print("QUIT!!!")
        pygame.quit()

    def fill(self):
        self.displayRegion.blit(self.frame, (0, 0))
        self.graphRegion.set_image(self.displayRegion)
        self.window_surface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()

    def handleEvent(self, event):
        '''
        parameter: if event is USEREVENT(pygame_gui event)

        if there is pop up window then pass this event let new window handle  
        if event type is button press verify what kind of button be pressed and handle it
            case 1 button is mode button control the layout of gui
            case 2 button is media button control the playing state of animation
            case 3 button is input button press these button will generate a new window
        if event type is selection list option be changed then get the new option and handle graph
        '''
        newWindowButton = [self.addnodebutton,
                           self.deletenodebutton, self.setpropertybutton, self.loadfilebutton, self.storefilebutton]
        if self.newWindowSurvive:
            self.handleNewWindow(event)
        elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in self.BtnOfAll:
                self.handleBtnState(event)
                self.handlePanelLayout()
            elif event.ui_element in self.BtnOfMedia:
                self.handleMediaState(event)
            elif self.newWindowSurvive == False and event.ui_element in newWindowButton:
                self.newWindow = self.createNewWindow(event)
                self.newWindowSurvive = self.newWindow.survive

        if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.selectionList:
            ind = self.getOptionInd(event.text)
            self.selectionState = SELECTIONSTATE[ind]
            self.handleGraph()
        self.handleMediaState(event)

    def handlePanelLayout(self):
        if self.btnState == HOMESTATE:
            # clear graph
            for panel in self.panelOfAll:
                if panel in self.panelOfHome:
                    panel.enable()
                    panel.show()
                else:
                    panel.disable()
                    panel.hide()

        elif self.btnState == ROUTINGSTATE:
            for panel in self.panelOfAll:
                if panel in self.panelOfRouting:
                    panel.enable()
                    panel.show()
                else:
                    panel.disable()
                    panel.hide()

    def handleBtnState(self, event):
        if event.ui_element == self.HomeBtn:
            self.HomeBtn.disable()
            self.routingBtn.enable()
            self.btnState = HOMESTATE
        elif event.ui_element == self.routingBtn:
            self.HomeBtn.enable()
            self.routingBtn.disable()
            self.btnState = ROUTINGSTATE
            print("handle event", self.mediaState)
            self.handleMediaBtnState()
        self.selectionList.set_item_list(self.optionList[self.btnState])

    def handleMediaBtnState(self):
        for v in self.mediaBtns[(self.mediaState[0], self.mediaState[1])]:
            if self.mediaBtns[(self.mediaState[0], self.mediaState[1])][v] == 1:
                v.enable()
            else:
                v. disable()

    def handleMediaState(self, event):
        '''
        INITSTATE = 2500
        NOTCOMPILESTATE = 2501
        COMPILESTATE = 2502
        PLAYSTATE = 2503
        PAUSESTATE = 2504
        DEFAULTSTATE = 2510
        ONLYSTATE = 2511
        FIRSTSTATE = 2512
        INTERMIDIATESTATE = 2513
        LASTSTATE = 2514
        NEXT = 2515
        PREVIOUS = 2516
        '''
        # print("media state", self.mediaState)
        if self.mediaState[0] == INITSTATE:
            if self.changed == False:
                self.changed = True
                print("Now in Initial State")
            if self.graph == None or self.graph.is_empty():
                #print("graph is empty")
                self.handleMediaBtnState()
            else:
                self.changed = False
                self.mediaState[0] = NOTCOMPILESTATE
                self.mediaState[1] = DEFAULTSTATE

        elif self.mediaState[0] == NOTCOMPILESTATE:
            if self.changed == False:
                self.changed = True
                print("Now in not compile State")
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.clearbutton:
                print("clear pressed")
                self.graph.clear()
                self.frame = self.graph.draw()
                self.mediaState[0] = INITSTATE
                self.mediaState[1] = DEFAULTSTATE
                self.changed = False
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and not(self.graph.is_compile) and event.ui_element == self.buildbutton and self.buildPress == False:
                print("Build pressed")
                self.buildPress = True
                # Algorithm = AdaptiveCS
                print(self.Algorithm_Class)
                self.animation = Animation(Algorithm_Class=self.Algorithm_Class, graph=self.graph,
                                           manager=self.manager, window_surface=self.window_surface, playState=self.mediaState, graphRegionOffset=(self.graphPanelOffsetX, self.graphPanelOffsetY+20), graphRegion=self.graphRegion, displayRegion=self.displayRegion, outputStream=self.console)
                self.animation.build(self.buildFinish)
                self.PlayPress = False
            elif self.buildFinish[0]:
                self.mediaState[0] = COMPILESTATE
                self.mediaState[1] = DEFAULTSTATE
                self.graph.compile_graph()
                print("media state 0 ", self.mediaState[0])
                self.chagned = False
                self.buildFinish[0] = False
                self.buildPress = False
                self.console.appendContent("Build Finish")
            else:
                self.handleMediaBtnState()

        elif self.mediaState[0] == COMPILESTATE:
            # self.handleMediaBtnState()
            if self.changed == False:
                self.changed = True
                print("Now in compile State")
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.clearbutton:
                self.graph.clear()
                self.frame = self.graph.draw()
                self.mediaState[0] = INITSTATE
                self.mediaState[1] = DEFAULTSTATE
                self.changed = False
            elif not(self.graph.is_compile):
                # add node del node set property will change the state
                self.changed = False
                self.mediaState[0] = NOTCOMPILESTATE
                self.mediaState[1] = DEFAULTSTATE
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.playbutton:
                self.finish[0] = False
                self.changed = False
                if len(self.animation.frames) == 1:
                    self.mediaState[0] = PLAYSTATE
                    self.mediaState[1] = ONLYSTATE
                    self.changed = False
                elif len(self.animation.frames) > 1:
                    self.mediaState[0] = PLAYSTATE
                    self.mediaState[1] = FIRSTSTATE
                    self.changed = False
                else:
                    print("Not define case")
                    print("frame len = ", len(self.animation.frames),
                          self.animation.frames)

                if(self.PlayPress == False):
                    self.PlayPress = True
                    print("In gui", self.finish)
                    t = threading.Thread(
                        target=self.animation.play, args=(self.finish,))
                    t.start()
                else:
                    self.PlayPress = False
                self.handleMediaBtnState()
                # self.animation.play([self.mediaState], self.speed, self.finish)
            else:
                self.handleMediaBtnState()
        elif self.mediaState[0] == PLAYSTATE:
            if self.finish[0]:
                self.mediaState[0] = COMPILESTATE
                self.mediaState[1] = DEFAULTSTATE
                self.changed = False
                self.PlayPress = False
            if self.mediaState[1] == ONLYSTATE:
                # create a thread and play the animation
                if self.changed == False:
                    self.changed = True
                    print("Now in play Only State")
                self.handleMediaBtnState()
            elif self.mediaState[1] == FIRSTSTATE:
                # identify media sub state in animation play function to know which frame current playing
                if self.changed == False:
                    self.changed = True
                    print("Now in play First State")
                self.handleMediaBtnState()
            elif self.mediaState[1] == INTERMIDIATESTATE:
                if self.changed == False:
                    self.changed = True
                    print("Now in play Intermidia State")
                self.handleMediaBtnState()
            elif self.mediaState[1] == LASTSTATE:
                self.handleMediaBtnState()
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.nextbutton:
                print("Press next")
                self.mediaState[0] = NEXT
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.previousbutton:
                print("Press previous")
                self.mediaState[0] = PREVIOUS
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.pausebutton:
                print("Press pause")
                self.mediaState[0] = PAUSESTATE
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.stopbutton:
                print("Press stop")
                self.mediaState[0] = COMPILESTATE
                self.mediaState[1] = DEFAULTSTATE
                print("change to compile in play stop")
                self.PlayPress = False
                self.handleMediaBtnState()
            else:
                pass

        elif self.mediaState[0] == PAUSESTATE:
            print("Now in pause state")
            if self.mediaState[1] == ONLYSTATE:
                self.handleMediaBtnState()
            elif self.mediaState[1] == FIRSTSTATE:
                self.handleMediaBtnState()
            elif self.mediaState[1] == INTERMIDIATESTATE:
                self.handleMediaBtnState()
            elif self.mediaState[1] == LASTSTATE:
                self.handleMediaBtnState()
            else:
                # media state is next or previous wait for animation process it
                self.handleMediaBtnState()
                pass
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.nextbutton:
                print("Press next")
                self.mediaState[0] = NEXT
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.previousbutton:
                print("Press previous")
                self.mediaState[0] = PREVIOUS
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.playbutton:
                print("Press previous")
                self.mediaState[0] = PLAYSTATE
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.stopbutton:
                print("Press stop")
                self.mediaState[0] = COMPILESTATE
                self.mediaState[1] = DEFAULTSTATE
                print("change to stop in pause")
                self.PlayPress = False
                self.handleMediaBtnState()
            else:
                pass
        else:
            pass

    def handleGraph(self):
        if self.btnState == HOMESTATE:
            if self.selectionState == SELECTIONSTATE[0]:

                pass
            elif self.selectionState == SELECTIONSTATE[1]:

                pass
        elif self.btnState == ROUTINGSTATE:
            if self.selectionState == SELECTIONSTATE[0]:
                # self.Algorithm_Class = Algorithm 0
                self.Algorithm_Class = AdaptiveCS
                pass
            elif self.selectionState == SELECTIONSTATE[1]:
                # self.Algorithm_Class = Algorithm 1
                self.Algorithm_Class = BFS
                pass
            elif self.selectionState == SELECTIONSTATE[2]:
                # self.Algorithm_Class = Algorithm 2
                self.Algorithm_Class = CS
                pass

    def getOptionInd(self, text):
        for ind in range(len(self.optionList[self.btnState])):
            if self.optionList[self.btnState][ind] == text:
                return ind

    def createNewWindow(self, event):
        self.newWindowSurvive = True
        if event.ui_element == self.addnodebutton:
            return AddNodeWindow(400, 400, self.manager, self.graph)
        elif event.ui_element == self.deletenodebutton:
            return DelNodeWindow(400, 400, self.manager, self.graph)
        elif event.ui_element == self.setpropertybutton:
            return SetPropertyWindow(400, 400, self.manager, self.graph)
        elif event.ui_element == self.loadfilebutton:
            return LoadFileDialogWindow(manager=self.manager, posx=100, posy=100, width=400, height=400)
        elif event.ui_element == self.storefilebutton:
            return StoreFileDialogWindow(manager=self.manager, posx=100, posy=100, width=400, height=400, graph=self.graph)

    def handleNewWindow(self, event):
        if self.newWindow.type == 'Add Node':
            self.newWindow.handleEvent(event)
            if self.newWindow.mode == 'Node' and self.newWindow.survive == False:
                if self.newWindow.is_valid:
                    print("Data is valid")
                    self.graph.add_node(nodeID=self.newWindow.nameValue,
                                        posX=self.newWindow.xValue, posY=self.newWindow.yValue)
            if self.newWindow.mode == 'Edge' and self.newWindow.survive == False:
                if self.newWindow.is_valid:
                    self.graph.add_edge(
                        edge=(self.newWindow.toValue, self.newWindow.fromValue), weight=self.newWindow.weightValue)
                    # self.frame = self.graph.draw()
        elif self.newWindow.type == 'Del Node':
            self.newWindow.handleEvent(event)
            if self.newWindow.mode == 'Node' and self.newWindow.survive == False:
                self.graph.del_node(self.newWindow.nameValue)
                self.frame = self.graph.draw()
                print("del ", self.newWindow.nameValue)
            elif self.newWindow.mode == 'Edge' and self.newWindow.survive == False:
                self.graph.del_edge(
                    (self.newWindow.toValue, self.newWindow.fromValue))
                self.frame = self.graph.draw()
                print("del edge", (self.newWindow.toValue, self.newWindow.fromValue))
        elif self.newWindow.type == 'Set':
            self.newWindow.handleEvent(event)
            if self.newWindow.is_valid:
                print("Set data is valid")
                print(self.newWindow.startValue)
                print(self.newWindow.destinationValue)
                print(self.newWindow.radiusValue)
                print(self.newWindow.MinSizeValue)
                self.graph.set_parameter(
                    key="Start", newValue=self.newWindow.startValue)
                self.graph.set_parameter(
                    key="Destination", newValue=self.newWindow.destinationValue)
                self.graph.set_parameter(
                    key="Radius", newValue=self.newWindow.radiusValue)
                self.graph.set_parameter(
                    key="MinSize", newValue=self.newWindow.MinSizeValue)
                for node in self.graph.nodesInfo:
                    self.graph.update_node_color(node, (0, 0, 255))
                self.graph.update_node_color(
                    self.graph.parasList['Start'], (0, 255, 0))

                self.graph.update_node_color(
                    self.graph.parasList['Destination'], (255, 0, 0))
        elif self.newWindow.type == 'Load File':
            self.newWindow.handleEvent(event)
            if self.newWindow.survive == False:
                if self.newWindow.is_valid:
                    print("Graph changed!!!")
                    self.graph = self.newWindow.graph

        elif self.newWindow.type == 'Store File':
            self.newWindow.handleEvent(event)
            if self.newWindow.survive == False:
                if self.newWindow.is_valid:
                    print("Store file")
        try:
            self.frame = self.graph.draw()
        except:
            print("Graph cannot be None")
        self.newWindowSurvive = self.newWindow.survive

    def run(self):
        is_running = True
        self.init_tracer()
        while is_running:
            time_delta = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    break
                if event.type == pygame.USEREVENT:
                    self.handleEvent(event)
                self.manager.process_events(event)
                self.manager.update(time_delta)
                self.update_tracer()
                self.tracer.process_events(event)
                if self.finish[0]:
                    self.fill()
                if not(self.finish[0]):
                    pass
            # self.manager.process_events(event)
            # self.manager.update(time_delta)
            # self.fill()
