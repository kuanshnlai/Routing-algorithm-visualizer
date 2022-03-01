import pygame
import pygame_gui
from basic_class.console import *


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
test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (240, 0), (100, 50)), text="test", manager=manager, object_id="#test_button", parent_element=hello_label)
content_panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(
    (0, 50), (800, 550)), manager=manager, starting_layer_height=0)

clock = pygame.time.Clock()
is_running = True
create = False
count = 0
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.ui_element == hello_button:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and not create:
                    tracer = ArrayTracer(width=300, height=300, manager=manager, object_id="#tracer",
                                         parent_element=content_panel, container=content_panel)
                    create = True
                    components = [tracer.label, tracer.label, tracer.label]
                    args = [{'height': 30, 'width': 50, "text": 'label1', "container": tracer.panel}, {'height': 30, 'width': 50,
                                                                                                       "text": 'label2', "container": tracer.panel}, {'height': 30, 'width': 50, "text": 'label3', "container": tracer.panel}]
                    tracer.set_title(components, args)
                elif create and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    components = [tracer.button, tracer.button, tracer.label]

                    args = [{'height': 50, 'width': 50, "text": str(count), "container": tracer.panel}, {'height': 50, 'width': 50,
                                                                                                         "text": str(count+1), "container": tracer.panel}, {'height': 50, 'width': 50, "text": str(count+2), "container": tracer.panel}]
                    count += 3
                    tracer.addNewRow(components, args)
                    # tracer.addComponent()
            elif event.ui_element == test_button:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    tracer.removeRow(1)
            else:
                if tracer != None:
                    tracer.process_events(event)
                    pass

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
