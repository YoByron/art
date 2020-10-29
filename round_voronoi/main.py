import numpy
from typing import List, Tuple
from geovoronoi import voronoi_regions_from_coords
import shapely.geometry

import pygame


WINDOW_SIZE = (1200, 800)
WINDOW_DIAGONAL = numpy.hypot(*WINDOW_SIZE)
WINDOW_RECT = pygame.Rect((0, 0), WINDOW_SIZE)
WINDOW_POLYGON = shapely.geometry.Polygon((
    WINDOW_RECT.topleft,
    WINDOW_RECT.topright,
    WINDOW_RECT.bottomright,
    WINDOW_RECT.bottomleft
))
FPS = 60
BACKGROUND_COLOR = pygame.Color(0, 32, 0)
CIRCLE_COLOR = pygame.Color(128, 96, 0)
CIRCLE_RADIUS = 5
LINE_WIDTH = 0
POLYGON_COLOR = pygame.Color(32, 128, 32)
CUT_RATIO = 0.25
CUT_ITERATIONS = 4


def generate_voronoi_polygons(points: List[Tuple[int, int]]) -> List[List[pygame.math.Vector2]]:
    # Does not work with less than 3 points.
    if len(points) < 3:
        return []
    poly_shapes = voronoi_regions_from_coords(
        numpy.asarray(points),
        WINDOW_POLYGON
    )[0]
    polygons = [poly.exterior.coords[:-1] for poly in poly_shapes]
    for i, polygon in enumerate(polygons):
        polygons[i] = [pygame.Vector2(p) for p in polygon]
    return polygons


def cut(
    points: List[pygame.math.Vector2],
    ratio: float,
    iterations: int = 1
) -> List[pygame.math.Vector2]:
    """ Chaikin's corner cutting: https://sighack.com/post/chaikin-curves
    ratio: Ratio (between 0 and 1) of the edge length which
        determines how close to the corner the cut should be made.
    iterations: Number of iterations of the cutting algorithm.
    """
    # Avoid cutting over the line midpoint:
    if ratio > 0.5:
        ratio = 1 - ratio

    for _ in range(iterations):
        new_points = []
        n = len(points)
        for i in range(n):
            a = points[i]
            b = points[(i + 1) % len(points)]
            new_points.append(a.lerp(b, ratio))
            new_points.append(b.lerp(a, ratio))
        points = new_points

    return points


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
                    polygons = generate_voronoi_polygons(points)
                    polygons = [cut(polygon, CUT_RATIO, CUT_ITERATIONS) for polygon in polygons]

        window.fill(BACKGROUND_COLOR)

        for polygon in polygons:
            pygame.draw.polygon(window, POLYGON_COLOR, polygon, LINE_WIDTH)

        for point in points:
            pygame.draw.circle(
                window,
                CIRCLE_COLOR,
                point,
                CIRCLE_RADIUS
            )

        pygame.display.flip()


if __name__ == "__main__":
    run()
