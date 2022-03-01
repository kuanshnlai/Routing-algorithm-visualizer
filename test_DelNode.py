import pygame
import pygame_gui
import random
import sys
from graph import *
from pop_up_window import *

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

# hello_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(
#     (0, 0), (40, 50)), text="Del", object_id="#hello_label", manager=manager)
del_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 0), (100, 50)),
                                          text='Del',
                                          manager=manager)

add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 0), (100, 50)),
                                          text='Add',
                                          manager=manager)

num = [1, 2, 3]
options = []
clock = pygame.time.Clock()
is_running = True
newWindow = False
g = graph(800, 550)
# g.add_node(100, 200)
# g.add_node(400, 300)
# g.add_node(300, 200)
# g.add_edge(("0", "1"))
# g.add_edge(("0", "2"))
# g.add_edge(("1", "2"))
# print(g.get_neighbor("0"))
# print(g.get_neighbor("1"))
# print(g.get_neighbor("2"))
frame = g.draw()
count = 0
survive = False
print(g)
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if survive == True:
                window.handleEvent(event)
                if window.survive == False:
                    if window.type == "Del Node":
                        if window.is_valid:
                            if window.mode == "Node":
                                name = window.nameValue
                                g.del_node(name)
                                print("After del node")
                                print("===========")
                                print(g)
                                print("===========")
                            elif window.mode == "Edge":
                                toNode = window.toValue
                                fromNode = window.fromValue
                                g.del_edge((toNode, fromNode))
                                print("After del edge")
                                print("===========")
                                print(g)
                                print("===========")
                    elif window.type == "Add Node":
                        if window.is_valid:
                            if window.mode == "Node":
                                g.add_node(nodeID=window.nameValue,
                                           posX=window.xValue, posY=window.yValue)
                                print("After add node")
                                print("===========")
                                print(g)
                                print("===========")
                            elif window.mode == "Edge":
                                print("After add edge")
                                print("===========")
                                print(g)
                                print("===========")
                                g.add_edge(
                                    edge=(window.toValue, window.fromValue), weight=window.weightValue)
                frame = g.draw()
                survive = window.survive
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == del_button:
                    window = DelNodeWindow(400, 400, manager, g)
                    survive = window.survive
                if event.ui_element == add_button:
                    window = AddNodeWindow(400, 400, manager, g)
                    survive = window.survive
        manager.process_events(event)

    manager.update(time_delta)

    # window_surface.blit(background, (0, 0))
    window_surface.blit(frame, (0, 50))
    manager.draw_ui(window_surface)

    pygame.display.update()
