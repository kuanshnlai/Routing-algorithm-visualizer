import pygame
import pygame_gui


class PopUpWindow:
    def __init__(self, width, height, manager, title=""):
        self.width = width
        self.height = height
        self.title = title
        self.manager = manager
        self.survive = True
        self.type = "Default"
        self.window = pygame_gui.elements.ui_window.UIWindow(
            pygame.Rect((100, 100), (self.width, self.height)), manager=self.manager, object_id="#Root")

    def add_button(self, text, posx, posy, width, height, parent, obj_id, container):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (posx, posy), (width, height)), text=text, container=container, parent_element=parent, manager=self.manager, object_id=obj_id)

    def add_panel(self, posx, posy, width, height, parent, obj_id, container):
        return pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((posx, posy), (width, height)), container=container, parent_element=parent, object_id=obj_id, manager=self.manager, starting_layer_height=1)

    def add_label(self, text, posx, posy, width, height, parent, obj_id, container):
        return pygame_gui.elements.UILabel(relative_rect=pygame.Rect(
            (posx, posy), (width, height)), manager=self.manager, text=text, container=container, parent_element=parent, object_id=obj_id)

    def add_dropdown_menu(self, posx, posy, width, height, parent, optionList, starting_option, obj_id, container):
        return pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect=pygame.Rect(
            (posx, posy), (width, height)), manager=self.manager, container=container, parent_element=parent, starting_option=starting_option, options_list=optionList, object_id=obj_id)

    def add_entryline(self, posx, posy, width, height, parent, obj_id, container):
        return pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((posx, posy), (width, height)), manager=self.manager, container=container, parent_element=parent, object_id=obj_id)

    def check_input(self):
        pass

    def kill(self):
        self.window.kill()
        self.survive = False

    def crate_error_promt_window(self, message):
        if message == '':
            print("POP up is valid")
            self.is_valid = True
            return
        self.error_window = pygame_gui.windows.ui_message_window.UIMessageWindow(
            rect=pygame.Rect((100, 100), (300, 200)), manager=self.manager, window_title="Error", html_message=message)
        self.is_valid = False

    def convertToInt(self, value):
        try:
            result = int(value)
        except:
            result = value
        return result

    def convertToStr(self, string):
        try:
            result = str(string)
        except:
            result = string
        return result


class AddNodeWindow(PopUpWindow):

    def __init__(self, width, height, manager, graph, title=""):
        super().__init__(width, height, manager, title="AddNode")
        self.type = "Add Node"
        self.mode = "Node"
        self.graph = graph

        # ---------Set ID
        self.nodePanelID = "#Node_panel"
        self.edgePanelID = "#Edge_panel"
        self.nodeButtonID = "#Node_button"
        self.edgeButtonID = "#Edge_button"
        self.nameLabelID = "#Name_label"
        self.xLabelID = "#X_label"
        self.yLabelID = "#Y_label"
        self.nameEntrylineID = "#Name_entryline"
        self.xEntrylineID = "#X_entryline"
        self.yEntrylineID = "#Y_entryline"
        self.nodeConfirmButtonID = "#Confirm_button"
        self.nodeCancelButtonID = "#Cancel_button"
        self.weightLabelID = "#Weight_label"
        self.toLabelID = "#To_label"
        self.fromLabelID = "#From_label"
        self.toPosLabelID = "#To_pos_label"
        self.fromPosLabelID = "#From_pos_label"
        self.edgeConfirmButtonID = "#Confirm_button"
        self.edgeCancelButtonID = "#Cancel_button"
        self.toDropdownMenuID = "#To_dropdown_menu"
        self.fromDropdownMenuID = "#From_dropdown_menu"

        # -------Default Value
        self.nameValue = None
        self.xValue = None
        self.yValue = None
        self.weightValue = None
        self.fromValue = None
        self.toValue = None

        self.create_all_elements()
        self.handleLayout()
        # print(self.graph)

    def handleLayout(self):
        if self.mode == "Node":
            self.nodeButton.disable()
            self.edgeButton.enable()
            self.nodePanel.show()
            self.edgePanel.hide()
        else:
            self.nodeButton.enable()
            self.edgeButton.disable()
            self.nodePanel.hide()
            self.edgePanel.show()

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT:
            # print("event type", event.user_type)
            # print("event element", event)
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.fromLabelID+"."+self.fromDropdownMenuID:
                    self.fromValue = event.text
                    nodeId = event.text
                    self.fromPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))
                elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.toLabelID+"."+self.toDropdownMenuID:
                    self.toValue = event.text
                    # nodeId = self.convertToInt(event.text)
                    nodeId = event.text
                    # print("nodeId", nodeId)
                    self.toPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))

            # ----------button pressed
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#Root"+"."+self.nodeButtonID:
                    self.mode = "Node"
                    self.handleLayout()
                elif event.ui_object_id == "#Root"+"."+self.edgeButtonID:
                    self.mode = "Edge"
                    self.handleLayout()
                elif event.ui_object_id == "#Root"+"."+self.nodePanelID+"."+self.nodeConfirmButtonID:
                    self.get_input_data()
                    self.check_input()
                    if self.is_valid:
                        self.kill()
                elif event.ui_object_id == "#Root"+"."+self.nodePanelID+"."+self.nodeCancelButtonID:
                    # print("Node cancel")
                    self.is_valid = False
                    self.kill()
                elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.edgeConfirmButtonID:
                    self.get_input_data()
                    # print("Weight", self.weightValue)
                    # print("From", self.fromValue)
                    # print("To", self.toValue)
                    self.check_input()
                    if self.is_valid:
                        self.kill()
                elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.edgeCancelButtonID:
                    # print("Edge cancel")
                    self.is_valid = False
                    self.kill()
                elif event.ui_object_id == "#Root"+"."+"#close_button":
                    self.is_valid = False
                    self.kill()
            # ---------Dropdown menu change

    def create_all_elements(self):
        print(self.nodePanelID)
        self.nodePanel = self.add_panel(
            posx=0, posy=50, width=400, height=275, parent=self.window, container=self.window, obj_id="#Node_panel")
        self.edgePanel = self.add_panel(
            posx=0, posy=50, width=400, height=275, parent=self.window, container=self.window, obj_id="#Edge_panel")
        self.nodeButton = self.add_button(text="Node",
                                          posx=50, posy=20, width=70, height=20, container=self.window, parent=self.window, obj_id="#Node_button")
        self.edgeButton = self.add_button(text="Edge",
                                          posx=130, posy=20, width=70, height=20, container=self.window, parent=self.window, obj_id="#Edge_button")
        # -------for node panel-------
        # add_label(self, text, posx, posy, width, height, parent, obj_id)
        # =====label
        self.nameLabel = self.add_label(
            text="Name", posx=50, posy=50, width=40, height=20, container=self.nodePanel, parent=self.nodePanel, obj_id="#Name_label")
        self.xLabel = self.add_label(
            text="X:  ", posx=50, posy=100, width=40, height=20, container=self.nodePanel, parent=self.nodePanel, obj_id="#X_label")
        self.yLabel = self.add_label(
            text="Y:  ", posx=50, posy=160, width=40, height=20, container=self.nodePanel, parent=self.nodePanel, obj_id="#Y_label")
        # =====input
        self.nameEntryline = self.add_entryline(
            posx=100, posy=50, width=70, height=20, container=self.nodePanel, parent=self.nameLabel, obj_id="#Name_entryline")
        self.xEntryline = self.add_entryline(
            posx=100, posy=100, width=70, height=20, container=self.nodePanel, parent=self.xLabel, obj_id="#X_entryline")
        self.yEntryline = self.add_entryline(
            posx=100, posy=160, width=70, height=20, container=self.nodePanel, parent=self.yLabel, obj_id="#Y_entryline")
        # =====button
        self.nodeConfirmButton = self.add_button(text="Confirm",
                                                 posx=70, posy=220, width=70, height=50, container=self.nodePanel, parent=self.nodePanel, obj_id="#Confirm_button")
        self.nodeCancelButton = self.add_button(text="Cancel",
                                                posx=160, posy=220, width=70, height=50, container=self.nodePanel, parent=self.nodePanel, obj_id="#Cancel_button")
        # -------for egde panel--------

        # =====label
        self.weightLabel = self.add_label(
            text="Weight:", posx=50, posy=50, width=60, height=20, container=self.edgePanel, parent=self.edgePanel, obj_id="#Weight_label")
        self.toLabel = self.add_label(
            text="To", posx=50, posy=100, width=60, height=20, container=self.edgePanel, parent=self.edgePanel, obj_id="#To_label")
        self.fromLabel = self.add_label(
            text="From", posx=50, posy=160, width=60, height=20, container=self.edgePanel, parent=self.edgePanel, obj_id="#From_label")
        self.toPosLabel = self.add_label(text="Pos:({:d},{:d})".format(
            0, 0), posx=210, posy=100, width=120, height=20, container=self.edgePanel, parent=self.toLabel, obj_id="#To_pos_label")
        self.fromPosLabel = self.add_label(text="Pos:({:d},{:d})".format(
            0, 0), posx=210, posy=160, width=120, height=20, container=self.edgePanel, parent=self.fromLabel, obj_id="#From_pos_label")

        # =====input
        self.weightEntryline = self.add_entryline(
            posx=120, posy=50, width=70, height=20, container=self.edgePanel, parent=self.weightLabel, obj_id="#Weight_entryline")
        nodeList = []
        for n in self.graph.nodesInfo:
            # if n == None:
            #     pass
            # else:
            #     nodeList.append(self.convertToStr(n))
            nodeList.append(n)
            print(n, ":", type(n))
        self.toDropdownMenu = self.add_dropdown_menu(
            posx=120, posy=100, width=90, height=20, container=self.edgePanel, parent=self.toLabel, obj_id="#To_dropdown_menu", starting_option="Default", optionList=nodeList)
        self.fromDropdownMenu = self.add_dropdown_menu(
            posx=120, posy=160, width=90, height=20, container=self.edgePanel, parent=self.fromLabel, obj_id="#From_dropdown_menu", starting_option="Default", optionList=nodeList)
        # =====button
        self.edgeConfirmButton = self.add_button(text="Confirm",
                                                 posx=70, posy=220, width=70, height=50, container=self.edgePanel, parent=self.edgePanel, obj_id="#Confirm_button")
        self.edgeCancelButton = self.add_button(text="Cancel",
                                                posx=160, posy=220, width=70, height=50, container=self.edgePanel, parent=self.edgePanel, obj_id="#Cancel_button")

    def get_input_data(self):
        if self.mode == "Node":
            self.nameValue = self.nameEntryline.get_text(
            ) if self.nameEntryline.get_text() != '' else None
            self.xValue = self.convertToInt(
                self.xEntryline.get_text()) if self.xEntryline.get_text() != '' else None
            self.yValue = self.convertToInt(
                self.yEntryline.get_text()) if self.yEntryline.get_text() != '' else None

        else:
            self.weightValue = self.convertToInt(self.weightEntryline.get_text(
            )) if self.weightEntryline.get_text() != '' else None

    def check_input(self):
        errorCount = 0
        errorMessage = ""
        # check if data is valid
        if self.mode == "Node":
            # Name      unique id
            # X         integer and 0<=X<=boundary
            # Y         integer and 0<=Y<=boundary
            # self.nameValue = self.convertToInt(self.nameValue)
            if self.nameValue == None:
                # print("Name can't be None")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Name can't be Empty<br/>".format(
                    errorCount))
                errorCount += 1
            elif self.nameValue in self.graph.nodesInfo:
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Name already exist<br/>".format(
                    errorCount))
                errorCount += 1

            # elif self.NameValue is valid data:

            if self.xValue == None:
                print("X can't be None")
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> X can't be Empty<br/>".format(errorCount))
                errorCount += 1

            elif type(self.xValue) != int:
                # print("X must be integer")
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> X must be integer<br/>".format(errorCount))
                errorCount += 1

            elif self.xValue < 0 or self.xValue > self.graph.width:
                # print("X must be positive and smaller than width")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> X must in range [{},{}]<br/>".format(
                    errorCount, 0, self.graph.width))
                errorCount += 1

            if self.yValue == None:
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> Y can't be Empty<br/>".format(errorCount))
                errorCount += 1

            elif type(self.yValue) != int:
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> Y must be integer<br/>".format(errorCount))
                errorCount += 1
            elif self.yValue < 0 or self.yValue > self.graph.height:
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Y must in range [{},{}]<br/>".format(
                    errorCount, 0, self.graph.height))
                errorCount += 1
            self.crate_error_promt_window(errorMessage)
        elif self.mode == "Edge":
            if self.weightValue == None:
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> Weight can't be Empty<br/>".format(errorCount))
                errorCount += 1
            elif type(self.weightValue) != int:
                errorMessage += (
                    "<font color=#FF0000 size=4>Error({}):</font> Weight must be integer<br/>".format(errorCount))
                errorCount += 1
            elif self.weightValue < 0:
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Weight must be positive<br/>".format(
                    errorCount))
                errorCount += 1

            if self.fromValue == None or self.fromValue == "Default":
                # print("From can't be None or \'Default\'")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> From can't be empty<br/>".format(
                    errorCount))
                errorCount += 1
            if self.toValue == None or self.toValue == "Default":
                # print("To can't be None or \'Default\'")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> To can't be empty<br/>".format(
                    errorCount))
                errorCount += 1

            if self.toValue != None and self.toValue != "Default" and self.fromValue != None and self.fromValue:
                if self.graph.exist_edge((self.fromValue, self.toValue)):
                    errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Edge already exist<br/>".format(
                        errorCount))
                    errorCount += 1
                if self.fromValue == self.toValue:
                    errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> To and from node must be different<br/>".format(
                        errorCount))
                    errorCount += 1
            self.crate_error_promt_window(errorMessage)


class DelNodeWindow(PopUpWindow):
    def __init__(self, width, height, manger, graph, title=""):
        super().__init__(width, height, manger, title)
        self.type = "Del Node"
        self.mode = "Node"
        self.graph = graph

        # Define IDs
        # =====panel======
        self.nodePanelID = "#Node_panel"
        self.edgePanelID = "#Edge_panel"
        # =====button=====
        self.nodeButtonID = "#Node_button"
        self.edgeButtonID = "#Edge_button"
        self.nodeConfirmButtonID = "#Confirm_button"
        self.nodeCancelButtonID = "#Cancel_button"
        self.edgeConfirmButtonID = "#Confirm_button"
        self.edgeCancelButtonID = "#Cancel_button"
        # ====entryline=====
        self.nameEntrylineID = "#Name_entryline"
        # ====label====
        self.nameLabelID = "#Name_label"
        self.fromLabelID = "#From_label"
        self.toLabelID = "#To_label"
        self.fromPosLabelID = "#From_pos_label"
        self.toPosLabelID = "#To_pos_label"
        # ====dropdown menu====
        self.fromDropdownMenuID = "#From_dropdown_menu"
        self.toDropdownMenuID = "#To_dropdown_menu"

        self.nameValue = None
        self.fromValue = None
        self.toValue = None

        self.create_all_elements()
        self.handleLayout()

    def handleLayout(self):
        if self.mode == "Node":
            self.nodeButton.disable()
            self.edgeButton.enable()
            self.nodePanel.show()
            self.edgePanel.hide()
        else:
            self.nodeButton.enable()
            self.edgeButton.disable()
            self.nodePanel.hide()
            self.edgePanel.show()

    def create_all_elements(self):
        print(self.nodePanelID)
        self.nodePanel = self.add_panel(
            posx=0, posy=50, width=400, height=275, parent=self.window, container=self.window, obj_id=self.nodePanelID)
        self.edgePanel = self.add_panel(
            posx=0, posy=50, width=400, height=275, parent=self.window, container=self.window, obj_id=self.edgePanelID)
        self.nodeButton = self.add_button(text="Node",
                                          posx=50, posy=20, width=70, height=20, container=self.window, parent=self.window, obj_id=self.nodeButtonID)
        self.edgeButton = self.add_button(text="Edge",
                                          posx=130, posy=20, width=70, height=20, container=self.window, parent=self.window, obj_id=self.edgeButtonID)

        # ========for node panel
        self.nameLabel = self.add_label(text="Name:", posx=50, posy=100, width=40, height=20,
                                        parent=self.nodePanel, container=self.nodePanel, obj_id=self.nameLabelID)
        self.nameEntryline = self.add_entryline(
            posx=100, posy=100, width=100, height=20, parent=self.nameLabel, obj_id=self.nameEntrylineID, container=self.nodePanel)
        self.nodeConfirmButton = self.add_button(text="Confirm",
                                                 posx=70, posy=220, width=70, height=50, container=self.nodePanel, parent=self.nodePanel, obj_id=self.nodeConfirmButtonID)
        self.nodeCancelButton = self.add_button(text="Cancel",
                                                posx=160, posy=220, width=70, height=50, container=self.nodePanel, parent=self.nodePanel, obj_id=self.nodeCancelButtonID)

        # =======for edge panel

        # =======label

        self.fromLabel = self.add_label(text="From:", posx=50, posy=50, width=40, height=20,
                                        parent=self.edgePanel, container=self.edgePanel, obj_id=self.fromLabelID)
        self.toLabel = self.add_label(text="To:", posx=50, posy=90, width=40, height=20,
                                      parent=self.edgePanel, container=self.edgePanel, obj_id=self.toLabelID)
        self.fromPosLabel = self.add_label(text="Pos:({:d},{:d})".format(
            0, 0), posx=210, posy=50, width=120, height=20, parent=self.fromLabel, container=self.edgePanel, obj_id=self.fromPosLabelID)
        self.toPosLabel = self.add_label(text="Pos:({:d},{:d})".format(
            0, 0), posx=210, posy=90, width=120, height=20, parent=self.toLabel, container=self.edgePanel, obj_id=self.toPosLabelID)
        # ========dropdown_menu
        nodeList = []
        for n in self.graph.nodes:
            if n == None:
                pass
            else:
                nodeList.append(self.convertToStr(n))
        self.fromDropdownMenu = self.add_dropdown_menu(posx=100, posy=50, width=100, height=20, parent=self.fromLabel,
                                                       optionList=nodeList, starting_option="Default", obj_id=self.fromDropdownMenuID, container=self.edgePanel)
        self.toDropdownMenu = self.add_dropdown_menu(posx=100, posy=90, width=100, height=20, parent=self.toLabel,
                                                     optionList=nodeList, starting_option="Default", obj_id=self.toDropdownMenuID, container=self.edgePanel)

        # ========button

        self.edgeConfirmButton = self.add_button(text="Confirm",
                                                 posx=70, posy=220, width=70, height=50, container=self.edgePanel, parent=self.edgePanel, obj_id="#Confirm_button")
        self.edgeCancelButton = self.add_button(text="Cancel",
                                                posx=160, posy=220, width=70, height=50, container=self.edgePanel, parent=self.edgePanel, obj_id="#Cancel_button")

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.fromLabelID+"."+self.fromDropdownMenuID:
                    self.fromValue = event.text
                    # nodeId = self.convertToInt(event.text)
                    nodeId = event.text
                    self.fromPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))
                elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.toLabelID+"."+self.toDropdownMenuID:
                    self.toValue = event.text
                    # nodeId = self.convertToInt(event.text)
                    nodeId = event.text
                    self.toPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))

        # ----------button pressed
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#Root"+"."+self.nodeButtonID:
                self.mode = "Node"
                self.handleLayout()
            elif event.ui_object_id == "#Root"+"."+self.edgeButtonID:
                self.mode = "Edge"
                self.handleLayout()
            elif event.ui_object_id == "#Root"+"."+self.nodePanelID+"."+self.nodeConfirmButtonID:
                self.get_input_data()
                # print("Name", self.nameValue)
                # print("X", self.xValue)
                # print("Y", self.yValue)
                self.check_input()
                if self.is_valid:
                    self.kill()
            elif event.ui_object_id == "#Root"+"."+self.nodePanelID+"."+self.nodeCancelButtonID:
                # print("Node cancel")
                self.is_valid = False
                self.kill()
            elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.edgeConfirmButtonID:
                self.get_input_data()
                # print("From", self.fromValue)
                # print("To", self.toValue)
                self.check_input()
                if self.is_valid:
                    self.kill()
            elif event.ui_object_id == "#Root"+"."+self.edgePanelID+"."+self.edgeCancelButtonID:
                # print("Edge cancel")
                self.is_valid = False
                self.kill()
            elif event.ui_object_id == "#Root"+"."+"#close_button":
                self.is_valid = False
                self.kill()

    def check_input(self):
        errorCount = 0
        errorMessage = ""
        # check if data is valid
        if self.mode == "Node":
            # Name      unique id
            if self.nameValue == None:
                # print("Name can't be None")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Name can't be Empty<br/>".format(
                    errorCount))
                errorCount += 1
            elif self.nameValue not in self.graph.nodesInfo:
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Name not exist<br/>".format(
                    errorCount))
                errorCount += 1
            self.crate_error_promt_window(errorMessage)
        elif self.mode == "Edge":
            if self.fromValue == None or self.fromValue == "Default":
                # print("From can't be None or \'Default\'")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> From can't be empty<br/>".format(
                    errorCount))
                errorCount += 1
            if self.toValue == None or self.toValue == "Default":
                # print("To can't be None or \'Default\'")
                errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> To can't be empty<br/>".format(
                    errorCount))
                errorCount += 1

            if self.toValue != None and self.toValue != "Default" and self.fromValue != None and self.fromValue:
                if not (self.graph.exist_edge((self.fromValue, self.toValue))):
                    errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Edge not exist<br/>".format(
                        errorCount))
                    errorCount += 1
            self.crate_error_promt_window(errorMessage)

    def get_input_data(self):
        if self.mode == "Node":
            self.nameValue = self.nameEntryline.get_text(
            ) if self.nameEntryline.get_text() != '' else None
        else:
            pass


class SetPropertyWindow(PopUpWindow):
    def __init__(self, width, height, manager, graph, title=""):
        super().__init__(width, height, manager, title="Set...")
        self.type = "Set"
        self.graph = graph
        self.is_valid = False
        # define object_id
        self.startLabelID = "#Start_label"
        self.destinationLabelID = "#Destination_label"
        self.radiusLabelID = "#Radius_label"
        self.MinSizeLabelID = "#MinSize_label"
        self.startPosLabelID = "#Start_pos_label"
        self.destinationPosLabelID = "#Destination_pos_label"

        self.confirmButtonID = "#Confirm_button"
        self.cancelButtonID = "#Cancel_button"

        self.radiusEntryLineID = "#Radius_entryline"
        self.MinSizeEntryLineID = "#MinSize_entryline"

        self.startDropdownMenuID = "#Start_dropdown_menu"
        self.destinationDropdownMenuID = "#Destination_dropdown_menu"

        # --- Default Value
        self.startValue = self.graph.parasList["Start"] if self.graph.parasList["Start"] != None else "Default"
        self.destinationValue = self.graph.parasList[
            "Destination"] if self.graph.parasList["Destination"] != None else "Default"
        # create all component
        self.create_all_elements()

    def create_all_elements(self):

        self.startLabel = self.add_label(
            text="Start:", posx=50, posy=50, width=90, height=20, parent=self.window, container=self.window, obj_id=self.startLabelID)
        self.destinationLabel = self.add_label(
            text="Destination", posx=50, posy=80, width=90, height=20, parent=self.window, container=self.window, obj_id=self.destinationLabelID)
        self.radiusLabel = self.add_label(
            text="Radius", posx=50, posy=110, width=90, height=20, parent=self.window, container=self.window, obj_id=self.radiusLabelID)
        self.minsizeLabel = self.add_label(
            text="MinSize", posx=50, posy=140, width=90, height=20, parent=self.window, container=self.window, obj_id=self.MinSizeLabelID)

        self.confirmButton = self.add_button(text="Confirm", posx=100, posy=280, width=70,
                                             height=50, container=self.window, parent=self.window, obj_id=self.confirmButtonID)
        self.cancelButton = self.add_button(text="Cancel", posx=220, posy=280, width=70,
                                            height=50, container=self.window, parent=self.window, obj_id=self.cancelButtonID)

        self.radiusEntryLine = self.add_entryline(
            posx=140, posy=110, width=60, height=20, parent=self.radiusLabel, container=self.window, obj_id=self.radiusEntryLineID)
        self.minsizeEntryLine = self.add_entryline(
            posx=140, posy=140, width=60, height=20, parent=self.minsizeLabel, container=self.window, obj_id=self.MinSizeEntryLineID)
        nodeList = []
        for n in self.graph.nodes:
            if n == None:
                pass
            else:
                nodeList.append(self.convertToStr(n))
        self.startDropdownMenu = self.add_dropdown_menu(
            posx=140, posy=50, width=90, height=20, parent=self.startLabel, container=self.window, obj_id=self.startDropdownMenuID, optionList=nodeList, starting_option=self.startValue)
        self.destinationDropdownMenu = self.add_dropdown_menu(
            posx=140, posy=80, width=90, height=20, parent=self.destinationLabel, container=self.window, obj_id=self.destinationDropdownMenuID, optionList=nodeList, starting_option=self.destinationValue)

        startPos = (self.graph.nodesInfo[self.startValue]['PosX'], self.graph.nodesInfo[self.startValue]['PosY']) if self.startValue != "Default" else (
            0, 0)
        destPos = (self.graph.nodesInfo[self.destinationValue]['PosX'], self.graph.nodesInfo[self.destinationValue]['PosY']) if self.destinationValue != "Default" else (
            0, 0)
        # startPos = (0, 0)
        # destPos = (0, 0)
        # print(self.startValue)
        # print(self.destinationValue)
        # print(self.graph.nodesInfo)
        self.startPosLabel = self.add_label(
            text="Pos:({:d},{:d})".format(startPos[0], startPos[1]), posx=240, posy=50, width=120, height=20, parent=self.startDropdownMenu, container=self.window, obj_id=self.startPosLabelID)
        self.destinationPosLabel = self.add_label(text="Pos:({:d},{:d})".format(
            destPos[0], destPos[1]), posx=240, posy=80, width=120, height=20, parent=self.destinationDropdownMenu, container=self.window, obj_id=self.destinationPosLabelID)

    def handleEvent(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.confirmButton:
                    self.get_input_data()
                    self.check_input()
                    if self.is_valid:
                        self.kill()
                elif event.ui_element == self.cancelButton:
                    self.is_valid = False
                    self.kill()
                elif event.ui_object_id == "#Root.#close_button":
                    self.is_valid = False
                    self.kill()
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.startDropdownMenu:
                    self.startValue = event.text
                    nodeId = event.text
                    self.startPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))
                elif event.ui_element == self.destinationDropdownMenu:
                    nodeId = event.text
                    self.destinationPosLabel.set_text(
                        'Pos:({},{})'.format(self.graph.nodesInfo[nodeId]['PosX'], self.graph.nodesInfo[nodeId]['PosY']))
                    self.destinationValue = event.text
                print(event.ui_object_id, "be changed")

    def get_input_data(self):

        self.radiusValue = self.radiusEntryLine.get_text(
        ) if self.radiusEntryLine.get_text() != '' else None
        self.MinSizeValue = self.minsizeEntryLine.get_text(
        ) if self.minsizeEntryLine.get_text() != '' else None

    def check_input(self):

        errorCount = 0
        errorMessage = ""
        # check if data is valid
        self.radiusValue = self.convertToInt(self.radiusValue)
        self.MinSizeValue = self.convertToInt(self.MinSizeValue)
        if self.radiusValue == None:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Radius can't be Empty<br/>".format(errorCount))
            errorCount += 1
        elif type(self.radiusValue) != int:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Radius must be integer<br/>".format(errorCount))
            errorCount += 1
        elif self.radiusValue <= 0 or self.radiusValue > 1000:
            errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> Radius must in range ({},{})<br/>".format(
                errorCount, 0, 1000))
            errorCount += 1

        if self.MinSizeValue == None:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Min size can't be Empty<br/>".format(errorCount))
            errorCount += 1
        elif type(self.MinSizeValue) != int:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Min size must be integer<br/>".format(errorCount))
            errorCount += 1
        elif self.MinSizeValue <= 0 or self.MinSizeValue > 200:
            errorMessage += ("<font color=#FF0000 size=4>Error({}):</font> MinSize must in range ({},{})<br/>".format(
                errorCount, 0, 200))
            errorCount += 1

        if self.startValue == "Default" or self.startValue == None:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Start can't be Empty<br/>".format(errorCount))
            errorCount += 1
        elif self.destinationValue == "Default" or self.destinationValue == None:
            errorMessage += (
                "<font color=#FF0000 size=4>Error({}):</font> Destination can't be Empty<br/>".format(errorCount))
            errorCount += 1
        self.crate_error_promt_window(errorMessage)
        if self.is_valid:
            print("Radius", self.radiusValue)
            print("MinSize", self.MinSizeValue)
            print("Start", self.startValue)
            print("Destination", self.destinationValue)

    def convertToInt(self, data):
        try:
            result = int(data)
        except:
            result = data
        return result
