import pygame
import pygame_gui


class Grid():
    def __init__(self, surface, width, height, gap):
        self.width = width
        self.height = height
        self.surface = surface
        self.newSurface = surface.copy()
        self.gap = gap

    def show(self):
        for i in range(0, self.width, self.gap):
            start_pos = (i, 0)
            end_pos = (i, self.height)
            pygame.draw.line(self.surface, (100, 10, 100),
                             start_pos, end_pos, 1)
        for i in range(0, self.height, self.gap):
            start_pos = (0, i)
            end_pos = (self.width, i)
            pygame.draw.line(self.surface, (100, 10, 100),
                             start_pos, end_pos, 1)
        return self.surface

    def hide(self):
        return self.newSurface


def drawGrid(width, height, gap, surface):
    for i in range(0, width, gap):
        start_pos = (i, 0)
        end_pos = (i, height)
        pygame.draw.line(surface, (100, 10, 100),
                         start_pos, end_pos, 1)
    for i in range(0, height, gap):
        start_pos = (0, i)
        end_pos = (width, i)
        pygame.draw.line(surface, (100, 10, 100),
                         start_pos, end_pos, 1)


def drawCircle(background, center):
    pygame.draw.circle(background, (0, 255, 0), center, 30, 1)


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))
window_surface.blit(background, (0, 0))

is_running = True
count = 0
press = False
clock = pygame.time.Clock()

grid = Grid(background, 800, 600, 50)
# PosLabel =  pygame_gui.elements.ui_label.UILabel()
manager = pygame_gui.UIManager((800, 600), 'data/themes/label.json')
button_rect = pygame.Rect((0, 0), (50, 50))
hello_button = pygame_gui.elements.UIButton(
    relative_rect=button_rect, text="Grid", object_id="#hello_button", manager=manager)
# small = pygame.Surface((80, 80))
# small.fill((255, 255, 255))
label_rect = pygame.Rect((0, 0), (80, 80))
label_rect.bottomright = (-20, -30)
hello_label = pygame_gui.elements.UILabel(relative_rect=label_rect, text="Hello", object_id="#hello_label", manager=manager, anchors={
                                          "left": 'right', "right": 'right', "top": 'bottom', "bottom": 'bottom'})
grid_background = background.copy()
origin_background = background.copy()
background = origin_background
drawGrid(800, 600, 50, grid_background)
drawCircle(origin_background, (100, 200))
drawCircle(grid_background, (100, 200))
while is_running:
    time_delta = clock.tick(60)/1000.0
    cur = pygame.mouse.get_pos()
    hello_label.set_text("({},{})".format(cur[0], cur[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hello_button:
                if not press:
                    background = grid_background
                    press = True
                else:
                    background = origin_background
                    press = False
                continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            center = pygame.mouse.get_pos()
            drawCircle(grid_background, center)
            drawCircle(origin_background, center)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(background)
    window_surface.blit(background, (0, 0))
    pygame.display.update()
