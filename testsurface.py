import pygame
import numpy

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))
window_surface.blit(background, (0, 0))
bit_array = pygame.surfarray.array2d(window_surface)
print(bit_array)
is_running = True
count = 0
bit_array = pygame.surfarray.array2d(window_surface)
print(type(bit_array))
print(type(window_surface))
if(isinstance(bit_array, numpy.ndarray)):
    print(True)
while is_running:
    # time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if count % 2 == 0:
                tmp_array = []
                for i in range(0, 100):
                    tmp_array.append([])
                    for j in range(0, 50):
                        tmp_array[i].append(bit_array[i][j])
                        bit_array[i][j] = 0
                        # print("change color")
                print(bit_array)
                pygame.surfarray.blit_array(window_surface, bit_array)
                print(tmp_array)
            else:
                for i in range(0, 100):
                    for j in range(0, 50):
                        bit_array[i][j] = tmp_array[i][j]
                pygame.surfarray.blit_array(window_surface, bit_array)
            count += 1
        # window_surface.blit(background, (0, 0))
        pygame.display.update()
