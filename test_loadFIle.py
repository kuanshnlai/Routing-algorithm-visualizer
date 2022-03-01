import pygame
import pygame_gui
import random
import sys
from graph import *
from pop_up_window import *
from load_network_file import *
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


clock = pygame.time.Clock()
is_running = True
g = graph(800, 550)
g.add_node(100, 200)
g.add_node(400, 300)
g.add_node(300, 200)
g.add_edge(("0", "1"))
g.add_edge(("0", "2"))
survive = False
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and not survive:
                if event.ui_element == hello_button:
                    file_dialog = StoreFileDialogWindow(
                        manager, 100, 100, 400, 400, g)
                    survive = file_dialog.survive
            if survive:
                file_dialog.handleEvent(event)
                survive = file_dialog.survive
            # elif not survive and file_dialog.graph != None:
            #     g = file_dialog.graph
            #     print(g)
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
