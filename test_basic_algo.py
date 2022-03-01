import pygame
import pygame_gui
import random
from graph import *
from pop_up_window import *
from curve import *
from algorithm import *
pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))
frame = background
manager = pygame_gui.UIManager((800, 600))

hello_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(
    (0, 0), (40, 50)), text="Hello", object_id="#hello_label", manager=manager)
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 0), (100, 50)),
                                            text='Say Hello',
                                            manager=manager, object_id="#hello_button", parent_element=hello_label)


test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 0), (100, 50)),
                                           text='test Hello',
                                           manager=manager, object_id="#test_button", parent_element=hello_label)
num = [1, 2, 3]
options = []

clock = pygame.time.Clock()
is_running = True
# curve = Curve((100, 200), (200, 200), 100, frame)
# curve.draw_curve(frame)
g = graph(800, 550)
g.add_node(100, 200)
g.add_node(400, 300)
g.add_node(300, 200)
g.add_edge(("0", "1"))
g.add_edge(("0", "2"))

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                algo = TestAlgorithm(g)
                frames = algo.run()
                for f in frames:
                    pygame.time.delay(1000)
                    window_surface.blit(f, (0, 50))
                    pygame.display.update()
                    manager.draw_ui(window_surface)
                    manager.update(time_delta)
                frame = frames[-1]
        manager.process_events(event)

    manager.update(time_delta)

    # window_surface.blit(background, (0, 0))
    window_surface.blit(frame, (0, 50))
    manager.draw_ui(window_surface)

    pygame.display.update()
