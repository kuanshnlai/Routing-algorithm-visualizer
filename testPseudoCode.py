import pygame
import pygame_gui
from basic_class.console import *
import re
import os
pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

hello_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(
    (0, 0), (40, 50)), text="Hello", object_id="#hello_label", manager=manager)
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 0), (100, 50)),
                                            text='Say Hello',
                                            manager=manager, object_id="#hello_button", parent_element=hello_label)


test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 0), (100, 50)),
                                           text='test Hello',
                                           manager=manager, object_id="#test_button", parent_element=hello_label)

clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 0), (100, 50)),
                                            text='clear',
                                            manager=manager, object_id="#test_button", parent_element=hello_label)

content = "Init"
panel = pygame_gui.elements.ui_panel.UIPanel(
    manager=manager, relative_rect=pygame.Rect((140, 50), (200, 300)), starting_layer_height=1)
textRegion = TextBox(html_text=content, manager=manager, window_surface=window_surface,
                     rect=pygame.Rect((140, 50), (400, 300)))
num = [1, 2, 3]
options = []

frames = []


def highlight(content):
    return "<font color=#ff0000>"+content+"</font>"


def func():
    frams.append("FunctionName")
    frames.append("Initial")
    frames.append("Name")
    frames.append("Result")


def switchContent(base, link_target):
    res = []
    with open(os.path.join(base, link_target)) as cur_file:
        for line in cur_file:
            res.append(line)
    for i in range(len(res)):
        res[i] = re.sub(r'\n', "", res[i])
    return res


file_path = "data/pseudoCode/"
file_data = ""
bfsPart = {}

codePart1 = "func(i):<br>"
codePart2 =\
    "if(i==1):<br>\
    return 1<br>"
codePart3 = \
    "elif(i==2):<br>\
    return 2<br>"
codePart4 =\
    "elif(i==3):<br>\
    return 3<br>"
codePart5 = \
    "elif(i==4):<br>\
    return 4<br>"
codePart6 =\
    "elif(i==5):<br>\
    return 5<br>"
codePart7 = \
    "elif(i==6):<br>\
    return 6<br>"
codePart8 =\
    "elif(i==8):<br>\
    return 8<br>"
codePart9 = \
    "elif(i==9):<br>\
    return 9<br>"
codePart = {1: codePart1, 2: codePart2, 3: codePart3,
            4: codePart4, 5: codePart5, 6: codePart6, 7: codePart7, 8: codePart8, 9: codePart9}
# bfsPart = {"FunctionName": bfsPart0, "Initial": bfsPart1,
#            "Main": bfsPart2, "Result": bfsPart3}
fileContent = []
base = "data/pseudoCode/"
with open(os.path.join(base, "adCS.html")) as cur_file:
    for line in cur_file:
        fileContent.append(line)
clock = pygame.time.Clock()
is_running = True
count = 0
finish = [False]
count = 0
for i in range(len(fileContent)):
    fileContent[i] = re.sub(r'\n', "", fileContent[i])
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            # print(event)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    textRegion.clear()
                    content = ""
                    for i in range(len(fileContent)):
                        if count == i:
                            highlightRate = (count/len(fileContent))
                            print("highlight me")
                            print("highlightRate = ", highlightRate)
                            content += highlight(fileContent[i])
                        else:
                            content += fileContent[i]
                    print("hello button")
                    textRegion.appendContent(content)
                    textRegion.moveToPos(highlightRate)
                if event.ui_element == test_button:
                    count += 1
                    count %= len(fileContent)
                if event.ui_element == clear_button:
                    finish[0] = True
                    textRegion.clear()
            if event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                print("link pressed")
                print(event.link_target)
                otherFileContent = switchContent(base, event.link_target)
                print("other", otherFileContent)
                textRegion.clear()
                content = ""
                for i in range(len(otherFileContent)):
                    if count == i:
                        # highlightRate = (count/len(otherFileContent))
                        print("highlight me")
                        # print("highlightRate = ", highlightRate)
                        content += highlight(otherFileContent[i])
                    else:
                        content += otherFileContent[i]
                    # print("hello button")
                textRegion.appendContent(content)
                textRegion.showContent()
                # textRegion.moveToPos(highlightRate)
                # print(content)
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    # window_surface.blit(frame, (0, 50))
    manager.draw_ui(window_surface)

    pygame.display.update()
