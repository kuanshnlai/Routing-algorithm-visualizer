import pygame
import pygame_gui
import random
import threading
from basic_class.graph import *
from basic_class.pop_up_window import *
from basic_class.curve import *
from basic_class.algorithm import *
from basic_class.animation import *
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

build_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 0), (100, 50)),
                                            text='test build',
                                            manager=manager, object_id="#build_button", parent_element=hello_label)
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 0), (100, 50)),
                                           text='test play',
                                           manager=manager, object_id="#play_button", parent_element=hello_label)
pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 0), (100, 50)),
                                            text='test pause',
                                            manager=manager, object_id="#pause_button", parent_element=hello_label)
next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 0), (100, 50)),
                                           text='test next',
                                           manager=manager, object_id="#next_button", parent_element=hello_label)
previous_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 0), (100, 50)),
                                               text='test previous',
                                               manager=manager, object_id="#test_previous", parent_element=hello_label)


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
g.add_node(600, 100)
g.add_edge(("0", "1"))
g.add_edge(("0", "2"))
playState = ["Init"]
finish = [True]
count = 0
print(type(finish))
mainThreadMode = "Normal"  # Normal or Animation
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == build_button:
                    animation = Animation(Algorithm_Class=TestAlgorithm, graph=g,
                                          manager=manager, window_surface=window_surface, playState=playState, graphRegionOffset=(0, 50))
                    animation.build()
                    print(len(animation.frames))
                    print("build sucess")
                    # build content test
                    # success
                    '''
                    for f in animation.frames:
                        pygame.time.delay(1000)
                        window_surface.blit(f, (0, 50))
                        pygame.display.update()
                        manager.draw_ui(window_surface)
                        manager.update(time_delta)
                    frame = animation.frames[len(animation.frames)-1]
                    '''
                elif event.ui_element == play_button and finish[0]:
                    th = threading.Thread(
                        target=animation.play, args=(finish,))
                    th.start()
                elif event.ui_element == play_button and not finish[0]:
                    playState[0] = "Play"
                elif event.ui_element == pause_button:
                    playState[0] = "Pause"
                elif event.ui_element == next_button:
                    # change state
                    playState[0] = "Next"
                    print("Next")
                    pass
                elif event.ui_element == previous_button:
                    # change state
                    playState[0] = "Previous"
                    print("Previous")
                    pass

                # th = threading.Thread(target=animation.build,args=())

        manager.process_events(event)

    manager.update(time_delta)
    if not(finish[0]):
        manager.draw_ui(window_surface)
        manager.update(time_delta)
        pygame.display.update()
    if finish[0]:
        # window_surface.blit(background, (0, 0))
        window_surface.blit(frame, (0, 50))
        manager.draw_ui(window_surface)
        pygame.display.update()
