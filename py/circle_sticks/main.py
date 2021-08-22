"""Inspired by https://www.reddit.com/r/generative/comments/mif9c1/the_seeker/"""


import numpy as np
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import pygame.freetype


WINDOW_SIZE = (1200, 800)
FPS = 60
UPS = 20
TIME_PER_UPDATE = 1 / UPS
BACKGROUND_COLOR = pygame.Color(32, 64, 64)
LINE_COLOR = pygame.Color(220, 220, 220)
MARKER_COLOR = pygame.Color(255, 32, 32)
CENTER = pygame.Vector2(WINDOW_SIZE) // 2
INNER_RADIUS = 175
OUTER_RADIUS = 375
INNER_N = 49
OUTER_N = 11
# interesting pairs: (49, 11), (300, 3), (600, 6), (12, 48), (42, 49), (60, 360), (480, 120)
INNER_ANGLES = np.linspace(0, 360, INNER_N, endpoint=False)
OUTER_ANGLES = np.linspace(0, 360, OUTER_N, endpoint=False)
OUTER_POINTS = [pygame.Vector2(0, -OUTER_RADIUS).rotate(angle) + CENTER for angle in OUTER_ANGLES]
INNER_POINTS = [pygame.Vector2(0, -INNER_RADIUS).rotate(angle) + CENTER for angle in INNER_ANGLES]
I_MAX = np.lcm(INNER_N, OUTER_N)  # number of iterations to draw all lines once

pygame.freetype.init()
FONT = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
FONT.fgcolor = pygame.Color(255, 255, 255)
FONT.bgcolor = BACKGROUND_COLOR
FONT_MARGIN = pygame.Vector2(5, 5)
FONT_LINE_SPACING = pygame.Vector2(0, FONT.get_sized_height())


def run() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("art: circle sticks")
    clock = pygame.time.Clock()
    canvas = pygame.Surface(WINDOW_SIZE)
    canvas.fill(BACKGROUND_COLOR)
    i = 0
    is_paused = True
    time_since_last_update = 0
    show_info = True

    # for i in range(INNER_N * OUTER_N):
    #     pygame.draw.aaline(canvas, LINE_COLOR, INNER_POINTS[i % INNER_N], OUTER_POINTS[i % OUTER_N])

    while True:
        dt = clock.tick(FPS) / 1000  # in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN and i < I_MAX:
                    is_paused = True
                    pygame.draw.aaline(
                        canvas,
                        LINE_COLOR,
                        INNER_POINTS[i % INNER_N],
                        OUTER_POINTS[i % OUTER_N]
                    )
                    i += 1
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_BACKSPACE:
                    canvas.fill(BACKGROUND_COLOR)
                    i = 0
                elif event.key == pygame.K_F1:
                    show_info = not show_info

        if not is_paused and i < I_MAX:
            time_since_last_update += dt
            while time_since_last_update > TIME_PER_UPDATE:
                time_since_last_update -= TIME_PER_UPDATE
                pygame.draw.aaline(
                    canvas,
                    LINE_COLOR,
                    INNER_POINTS[i % INNER_N],
                    OUTER_POINTS[i % OUTER_N]
                )
                i += 1
        window.blit(canvas, (0, 0))

        if i < I_MAX:
            # draw the marker one step ahead
            marker_inner_i = i % INNER_N
            marker_outer_i = i % OUTER_N
            pygame.draw.aaline(
                window,
                MARKER_COLOR,
                INNER_POINTS[marker_inner_i],
                OUTER_POINTS[marker_outer_i]
            )
            pygame.draw.circle(window, MARKER_COLOR, INNER_POINTS[marker_inner_i], 4)
            pygame.draw.circle(window, MARKER_COLOR, OUTER_POINTS[marker_outer_i], 4)

        if show_info:
            FONT.render_to(
                window,
                FONT_MARGIN,
                f"FPS: {clock.get_fps():.0f}"
            )
            FONT.render_to(
                window,
                FONT_MARGIN + FONT_LINE_SPACING,
                f"UPS: {0 if is_paused else UPS}"
            )
            FONT.render_to(
                window,
                FONT_MARGIN + FONT_LINE_SPACING * 2,
                f"i: {i}"
            )
            FONT.render_to(
                window,
                FONT_MARGIN + FONT_LINE_SPACING * 3,
                f"progress: {i / I_MAX * 100:.1f} %"
            )

        pygame.display.flip()


if __name__ == "__main__":
    run()
