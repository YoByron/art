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
CIRCLE_COLOR = pygame.Color(255, 0, 0)
CIRCLE_RADIUS = 5
LINE_WIDTH = 3
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
    polygons = []
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

        keep = []
        for i, (p, mv) in enumerate(zip(points, move_vectors)):
            x = p[0] + (mv[0] * dt)
            y = p[1] + (mv[1] * dt)
            points[i] = (x, y)
            if WINDOW_RECT.collidepoint(x, y):
                keep.append(i)
        points = [points[i] for i in keep]
        move_vectors = [move_vectors[i] for i in keep]

        polygons = voronoi.generate_voronoi_polygons(
            points,
            WINDOW_POLYGON
        )
        polygons = [
            corner_cutter.cut(polygon, CUT_RATIO, CUT_ITERATIONS)
            for polygon in polygons
        ]

        window.fill(BACKGROUND_COLOR)
        for polygon in polygons:
            pygame.draw.polygon(window, POLYGON_FILL_COLOR, polygon)
            if DRAW_OUTLINES:
                pygame.draw.polygon(window, POLYGON_LINE_COLOR, polygon, LINE_WIDTH)
        for point in points:
            pygame.draw.circle(window, CIRCLE_COLOR, point, CIRCLE_RADIUS)
        pygame.draw.rect(window, POLYGON_LINE_COLOR, WINDOW_RECT, LINE_WIDTH)

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
