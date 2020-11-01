import os
import sys
from typing import Tuple
import math
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import pygame.freetype

sys.path.append(os.getcwd())
from helpers import corner_cutter
from helpers import voronoi


SHOW_DEBUG_INFO = True
WINDOW_SIZE = (1200, 800)
WINDOW_RECT = pygame.Rect((0, 0), WINDOW_SIZE)
WINDOW_POLYGON = voronoi.rect_to_shapely_polygon(WINDOW_RECT)
FPS = 60
BACKGROUND_COLOR = pygame.Color(0, 255, 255)
CIRCLE_COLOR = pygame.Color(0, 255, 255)
CIRCLE_RADIUS = 5
LINE_WIDTH = 3
BORDER_WIDTH = 10
DRAW_OUTLINES = True
POLYGON_FILL_COLOR = pygame.Color(32, 32, 32)
POLYGON_LINE_COLOR = pygame.Color(0, 255, 255)
CUT_RATIO = 0.15
CUT_ITERATIONS = 3
SPEED_MODIFIER = 50
SPREAD = 50
NUM_CIRCLES_PER_RIGHT_CLICK = 50


def get_move_vector(point: Tuple[int, int]) -> Tuple[float, float]:
    dx = point[0] - WINDOW_RECT.centerx
    dy = point[1] - WINDOW_RECT.centery
    length = math.hypot(dx, dy) / SPEED_MODIFIER
    return dx / length, dy / length


def run() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("art: round voronoi")
    clock = pygame.time.Clock()
    font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
    font.fgcolor = pygame.Color(255, 255, 255)
    font.bgcolor = POLYGON_FILL_COLOR
    points = []
    move_vectors = []

    # DEBUG:
    points = [(580, 200), (500, 370), (730, 310), (600, 290)]
    move_vectors = [get_move_vector(p) for p in points]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points.append(event.pos)
                    move_vectors.append(get_move_vector(event.pos))
                elif event.button == 3:
                    for _ in range(NUM_CIRCLES_PER_RIGHT_CLICK):
                        x, y = event.pos
                        x += random.randint(-SPREAD, SPREAD)
                        y += random.randint(-SPREAD, SPREAD)
                        points.append((x, y))
                        move_vectors.append(get_move_vector((x, y)))

        for i, (p, mv) in reversed(list(enumerate(zip(points, move_vectors)))):
            # Iterate backwards because the lengths change while iterating.
            x = p[0] + (mv[0] * dt)
            y = p[1] + (mv[1] * dt)
            if WINDOW_RECT.collidepoint(x, y):
                points[i] = (x, y)
            else:
                del points[i]
                del move_vectors[i]

        polygons = voronoi.generate_voronoi_polygons(
            points,
            WINDOW_POLYGON
        )
        polygons = [
            corner_cutter.cut(polygon, CUT_RATIO, CUT_ITERATIONS)
            for polygon in polygons
        ]

        if len(points) > 2:
            window.fill(BACKGROUND_COLOR)
        else:
            # Voronoi does not work with less than three points.
            window.fill(POLYGON_FILL_COLOR)
        for polygon in polygons:
            pygame.draw.polygon(window, POLYGON_FILL_COLOR, polygon)
            if DRAW_OUTLINES:
                pygame.draw.polygon(window, POLYGON_LINE_COLOR, polygon, LINE_WIDTH)
        for point in points:
            pygame.draw.circle(window, CIRCLE_COLOR, point, CIRCLE_RADIUS)
        pygame.draw.rect(window, POLYGON_LINE_COLOR, WINDOW_RECT, BORDER_WIDTH)

        if SHOW_DEBUG_INFO:
            font.render_to(
                window,
                (5, 5),
                f"fps: {clock.get_fps():.0f}"
            )
            font.render_to(
                window,
                (5, 25),
                f"{len(polygons)=}"
            )
            font.render_to(
                window,
                (5, 45),
                f"{sum(len(p) for p in polygons)=}"
            )

        pygame.display.flip()


if __name__ == "__main__":
    run()
