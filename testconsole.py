import pygame_gui
import pygame
from basic_class.console import *
import threading

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
                     rect=pygame.Rect((140, 50), (200, 300)))
num = [1, 2, 3]
options = []


def func(outputStream, count):
    for i in range(count):
        outputStream('*')
        # manager.draw_ui(window_surface)
        # pygame.display.update()
        time.sleep(0.2)


def function2(count):
    for i in range(count):
        print("In function2 print", i)
        time.sleep(0.1)


# for i in num:
#     options.append(str(i))
# test_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect=pygame.Rect(
#     (90, 0), (40, 50)), manager=manager, starting_option="0", options_list=options)
clock = pygame.time.Clock()
is_running = True
count = 0
finish = [False]
while is_running:
    time_delta = clock.tick(60)/1000.0
    # count += 1
    # if(count % 20 == 0):
    #     textRegion.appendContent(str(count))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print("hello button")
                    textRegion.appendContent("hello button pressed")
                if event.ui_element == test_button:
                    # func(manager, window_surface, textRegion.appendContent, 30)
                    # func(sys.stdout.write, 30)
                    finish[0] = False
                    t = threading.Thread(
                        target=func, args=(print, 30,))
                    # textRegion.simpleProcessBar(30)
                    t.start()
                    s = threading.Thread(target=function2, args=(30,))
                    s.start()
                if event.ui_element == clear_button:
                    finish[0] = True
                    textRegion.clear()

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    # window_surface.blit(frame, (0, 50))
    manager.draw_ui(window_surface)

    pygame.display.update()
