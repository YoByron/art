# https://www.youtube.com/watch?v=ZI1dmHv3MeM


# from perlin_noise import PerlinNoise
# import matplotlib.pyplot as plt
#
# noise = PerlinNoise()
# xpix, ypix = 10, 10
# pic = [[noise((i/xpix, j/ypix)) for i in range(xpix)] for j in range(ypix)]
# for row in pic:
#     print(row)
# plt.imshow(pic, cmap="gray")
# plt.show()


import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


WINDOW_SIZE = (1200, 800)
FPS = 60
BACKGROUND_COLOR = pygame.Color("#004080")
LINE_COLOR = pygame.Color("#dddddd")
CIRCLE_CENTER = pygame.Vector2(WINDOW_SIZE) / 2
NUMBER_OF_POINTS = 7
RADIUS = 200
angle_increment = 360 / NUMBER_OF_POINTS
angles = (i * angle_increment for i in range(NUMBER_OF_POINTS))
circle_points = [pygame.Vector2(RADIUS, 0).rotate(angle) + CIRCLE_CENTER for angle in angles]


def run():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        window.fill(BACKGROUND_COLOR)
        pygame.draw.aalines(window, LINE_COLOR, True, circle_points)
        pygame.display.flip()


run()
