# TODO: Apply some noise to the cut_ratio and draw the polygons with alpha
#  to give them a fuzzy edge.

import pygame

from helpers import corner_cutter
from helpers import voronoi


WINDOW_SIZE = (1200, 800)
WINDOW_POLYGON = voronoi.rect_to_shapely_polygon(pygame.Rect((0, 0), WINDOW_SIZE))
FPS = 60
BACKGROUND_COLOR = pygame.Color(0, 32, 0)
CIRCLE_COLOR = pygame.Color(255, 128, 0)
CIRCLE_RADIUS = 5
LINE_WIDTH = 3
DRAW_OUTLINES = True
POLYGON_FILL_COLOR = pygame.Color(32, 128, 32)
POLYGON_LINE_COLOR = pygame.Color(0, 255, 255)
CUT_RATIO = 0.15
CUT_ITERATIONS = 4


def run() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("art: round voronoi")
    clock = pygame.time.Clock()
    points = []
    polygons = []

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points.append(event.pos)
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
        pygame.display.flip()


if __name__ == "__main__":
    run()
